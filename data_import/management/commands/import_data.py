import logging
import os
import aiohttp
import asyncio
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from data_import.marketsharp_api import MarketSharpAPI
from data_import.data_processor import DataProcessor
from data_import.registry import ProcessorRegistry
from datetime import datetime as DateTime
from typing import Optional, Dict, Any, List
import random

logger = logging.getLogger(__name__)
BATCH_SIZE = 5000
INITIAL_CONCURRENT_FETCHES = 3  # Reduced from 5
MIN_CONCURRENT_FETCHES = 1
MAX_RETRY_DELAY = 30
INITIAL_RETRY_DELAY = 10

class Command(BaseCommand):
    help = 'Imports data from MarketSharp API and processes it sequentially for each endpoint.'

    def __init__(self, logger: Optional[logging.Logger] = None):
        super().__init__()
        self._logger = logger or logging.getLogger(__name__)
        if not logger:
            logging.basicConfig(level=logging.DEBUG)
        self.registry = ProcessorRegistry.get_instance()
        self.current_concurrent_fetches = INITIAL_CONCURRENT_FETCHES

    def add_arguments(self, parser):
        parser.add_argument(
            '--endpoint', 
            type=str, 
            choices=list(self.registry.endpoints.keys()),  
            help='Specify which endpoint to fetch data from. Leave empty to fetch all.'
        )
        parser.add_argument(
            '--max-concurrent',
            type=int,
            default=INITIAL_CONCURRENT_FETCHES,
            help=f'Maximum number of concurrent page fetches (default: {INITIAL_CONCURRENT_FETCHES})'
        )

    async def get_latest_update(self, endpoint: str) -> DateTime:
        static_endpoints = {
            "companies", "activity_references", "addresses", 
            "appointment_results", "contact_phones", "contact_types",
            "custom_fields", "product_details", "product_types", 
            "product_interests", "inquiry_statuses", "inquiry_source_primaries",
            "inquiry_source_secondaries"
        }
        
        if endpoint not in static_endpoints:
            model_class = self.registry.models[endpoint]
            latest_update = await sync_to_async(
                model_class.objects.order_by('-last_update').values_list('last_update', flat=True).first
            )()
            latest_update = latest_update if latest_update else DateTime(1970, 1, 1)
        else:
            latest_update = ""
        return latest_update

    def handle(self, *args: Any, **options: Dict[str, Any]):
        logging.basicConfig(level=logging.INFO)
        endpoint = options.get('endpoint')
        max_concurrent = options.get('max_concurrent', INITIAL_CONCURRENT_FETCHES)
        asyncio.run(self.async_handle(endpoint, max_concurrent))

    async def async_handle(self, endpoint: Optional[str] = None, max_concurrent: int = INITIAL_CONCURRENT_FETCHES):
        if endpoint:
            await self.process_endpoint(endpoint, max_concurrent)
        else:
            for ep in self.registry.endpoints.keys():
                self._logger.info(f"Starting processing for endpoint: {ep}")
                await self.process_endpoint(ep, max_concurrent)
                self._logger.info(f"Completed processing for endpoint: {ep}")

    async def process_endpoint(self, endpoint: str, max_concurrent: int):
        start_time = DateTime.now()
        
        credentials = {
            'secret_key': os.getenv('MARKETSHARP_SECRET_KEY'),
            'api_key': os.getenv('MARKETSHARP_API_KEY'),
            'company_id': os.getenv('MARKETSHARP_COMPANY_ID')
        }
        
        if not all(credentials.values()):
            self._logger.error("Missing required API credentials")
            return

        url = self.registry.endpoints[endpoint]
        latest_update = await self.get_latest_update(endpoint)

        self._logger.info(f"Started fetching {endpoint} from MarketSharp API (after {latest_update})")
        
        ms_api = MarketSharpAPI(credentials['company_id'], 
                               credentials['api_key'], 
                               credentials['secret_key'], 
                               self._logger)
        data_processor = DataProcessor(self._logger)
        processor_class = self.registry.processors[endpoint]
        processor = processor_class(self._logger, data_processor)

        async with aiohttp.ClientSession() as session:
            try:
                total_processed = await self.fetch_and_process_paginated_data(
                    session=session,
                    ms_api=ms_api,
                    processor=processor,
                    endpoint=endpoint,
                    url=url,
                    latest_update=latest_update,
                    max_concurrent=max_concurrent
                )
                duration = DateTime.now() - start_time
                self._logger.info(
                    f"Finished processing {endpoint}. "
                    f"Total records: {total_processed}. Duration: {duration}."
                )
            except Exception as e:
                self._logger.error(f"Error processing {endpoint}: {str(e)}", exc_info=True)

    async def fetch_with_retry(self, session, ms_api, url, latest_update, skip, max_retries=5):
        """Fetch a single page with exponential backoff retry."""
        retry_delay = INITIAL_RETRY_DELAY
        attempt = 1

        while attempt <= max_retries:
            try:
                self._logger.debug(f"Fetching page: {url}, skip {skip}, attempt {attempt}")
                data = await ms_api.get_data(session, url, latest_update, skip=skip)
                return data
            except aiohttp.ClientResponseError as e:
                if e.status == 503:
                    if attempt < max_retries:
                        # Add jitter to prevent thundering herd
                        jitter = random.uniform(0.5, 1.5)
                        delay = min(retry_delay * jitter, MAX_RETRY_DELAY)
                        self._logger.warning(
                            f"503 Service Unavailable. Retrying after {delay:.1f} seconds... "
                            f"(attempt {attempt}/{max_retries})"
                        )
                        await asyncio.sleep(delay)
                        retry_delay *= 2  # Exponential backoff
                        attempt += 1
                        continue
                raise
            except Exception as e:
                self._logger.error(f"Error fetching page (skip={skip}): {str(e)}")
                raise

    async def fetch_batch(self, session, ms_api, url, latest_update, skip_values: List[int]):
        """Fetch a batch of pages with rate limiting."""
        tasks = [
            self.fetch_with_retry(session, ms_api, url, latest_update, skip)
            for skip in skip_values
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count failures
        failures = sum(1 for r in results if isinstance(r, Exception))
        
        # Adjust concurrent fetches based on failures
        if failures > len(results) / 2:
            self.current_concurrent_fetches = max(
                MIN_CONCURRENT_FETCHES,
                self.current_concurrent_fetches - 1
            )
            self._logger.info(
                f"Too many failures, reducing concurrent fetches to {self.current_concurrent_fetches}"
            )
        
        return results

    async def fetch_and_process_paginated_data(self, session, ms_api, processor, 
                                             endpoint, url, latest_update, max_concurrent):
        """Fetch and process paginated data with dynamic concurrency adjustment."""
        skip = 0
        total_records_processed = 0
        self.current_concurrent_fetches = max_concurrent
        
        while True:
            # Calculate skip values for this batch
            skip_values = [
                skip + i * BATCH_SIZE 
                for i in range(self.current_concurrent_fetches)
            ]
            
            # Fetch batch of pages
            batch_results = await self.fetch_batch(
                session, ms_api, url, latest_update, skip_values
            )
            
            # Process results sequentially
            has_data = False
            for result in batch_results:
                if isinstance(result, Exception):
                    continue
                    
                if not result:
                    continue
                    
                has_data = True
                try:
                    num_records = await processor.process_objects(result, BATCH_SIZE)
                    records_count = (
                        num_records.total_processed 
                        if hasattr(num_records, 'total_processed')
                        else num_records
                    )
                    
                    if not isinstance(records_count, int):
                        raise TypeError(
                            f"Unexpected return type from process_objects: {type(records_count)}"
                        )
                        
                    total_records_processed += records_count
                    self._logger.info(
                        f"Processed {records_count} {endpoint}. "
                        f"Total processed: {total_records_processed}"
                    )

                    if records_count < BATCH_SIZE:
                        return total_records_processed
                        
                except Exception as e:
                    self._logger.error(f"Error processing batch: {str(e)}", exc_info=True)
            
            if not has_data:
                return total_records_processed
                
            skip += BATCH_SIZE * self.current_concurrent_fetches