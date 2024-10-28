from typing import List, Dict, Any, Tuple, Optional, Set
from django.db import transaction
from asgiref.sync import sync_to_async
from uuid import UUID
from datetime import datetime
from dateutil.parser import parse as parse_date
import logging
from enum import Enum
from dataclasses import dataclass
from functools import lru_cache

class FieldType(Enum):
    UUID = 'uuid'
    DATETIME = 'datetime'
    BOOLEAN = 'boolean'
    INTEGER = 'int'
    FLOAT = 'float'
    DECIMAL = 'decimal'
    STRING = 'string'

@dataclass
class ProcessingResult:
    total_processed: int = 0
    successful: int = 0
    failed: int = 0
    errors: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

@dataclass
class FieldMapping:
    xml_field: str
    model_field: str
    field_type: FieldType
    required: bool = False
    default: Any = None
    is_primary_key: bool = False

    def __post_init__(self):
        if isinstance(self.field_type, str):
            self.field_type = FieldType(self.field_type)
        if self.required and self.default is not None:
            raise ValueError(f"Field {self.model_field} cannot be both required and have a default value")

class BaseProcessor:
    def __init__(self, logger: logging.Logger, data_processor):
        self.logger = logger
        self.data_processor = data_processor

    @staticmethod
    def is_valid_uuid(val: str) -> bool:
        if not val:
            return False
        try:
            UUID(val)
            return True
        except (ValueError, AttributeError):
            return False

    def parse_value(self, value: str, field_type: FieldType, field_name: str) -> Any:
        """Parse field value with enhanced type handling and validation."""
        if value is None:
            return None
            
        try:
            if field_type == FieldType.UUID:
                return UUID(value) if self.is_valid_uuid(value) else None
            elif field_type == FieldType.DATETIME:
                return parse_date(value) if value else None
            elif field_type == FieldType.BOOLEAN:
                return value.lower() == 'true' if value else False
            elif field_type == FieldType.INTEGER:
                return int(value) if value else None
            elif field_type == FieldType.FLOAT:
                return float(value) if value else None
            elif field_type == FieldType.DECIMAL:
                return float(value) if value else None
            elif field_type == FieldType.STRING:
                return value or ''
            return value
        except Exception as e:
            self.logger.warning(f"Failed to parse {field_name} ({field_type.value}): {str(e)}")
            return None

    @lru_cache(maxsize=100)
    def get_model_fields(self, model) -> Set[str]:
        """Cache model fields to improve performance."""
        return {field.name for field in model._meta.fields if not field.primary_key}

    def extract_data(self, properties, field_mappings: Dict[str, FieldMapping]) -> Dict[str, Any]:
        """Extract and validate data from XML properties."""
        if properties is None:
            self.logger.error("No properties found in XML")
            return {}

        data = {}
        has_required_fields = True

        for key, mapping in field_mappings.items():
            value = self.data_processor.get_xml_text(properties, mapping.xml_field)
            parsed_value = self.parse_value(value, mapping.field_type, key)

            if mapping.required and parsed_value is None:
                self.logger.error(f"Missing required field: {key}")
                has_required_fields = False
                continue

            data[mapping.model_field] = parsed_value if parsed_value is not None else mapping.default

        return data if has_required_fields else {}

    async def process_entries(
        self,
        entries: List[Any],
        model,
        field_mappings: Dict[str, FieldMapping],
        batch_size: int
    ) -> int:
        """Process entries with support for models with or without primary keys."""
        result = ProcessingResult(
            total_processed=len(entries),
            successful=0,
            failed=0,
            errors=[]
        )

        try:
            # Find primary key mapping if it exists
            pk_mapping = next(
                (mapping for mapping in field_mappings.values() if mapping.is_primary_key),
                None
            )
            
            valid_records = []
            record_ids = []

            # Process entries in chunks for better memory management
            for i in range(0, len(entries), batch_size):
                chunk = entries[i:i + batch_size]
                for entry in chunk:
                    properties = entry.find('.//m:properties', namespaces=self.data_processor.nsmap)
                    data = self.extract_data(properties, field_mappings)
                    
                    if data:
                        if pk_mapping:
                            pk_value = data.get(pk_mapping.model_field)
                            if pk_value:
                                valid_records.append((pk_value, data))
                                record_ids.append(pk_value)
                            else:
                                result.failed += 1
                        else:
                            # For models without primary key, just store the data
                            valid_records.append((None, data))
                    else:
                        result.failed += 1

            if not valid_records:
                return result.successful

            # Handle records based on whether we have primary keys
            if pk_mapping:
                # Fetch existing records
                existing_records = await sync_to_async(lambda: set(
                    model.objects.filter(id__in=record_ids).values_list('id', flat=True)
                ))()

                # Prepare records for database operations
                records_to_insert = []
                records_to_update = []

                for pk_value, data in valid_records:
                    if pk_value in existing_records:
                        records_to_update.append(model(**data))
                    else:
                        records_to_insert.append(model(**data))
            else:
                # For models without primary key, all records are new insertions
                records_to_insert = [model(**data) for _, data in valid_records]
                records_to_update = []

            # Perform database operations
            await self.bulk_operations(model, records_to_insert, records_to_update, batch_size)
            result.successful = len(valid_records)

        except Exception as e:
            self.logger.error(f"Error processing entries: {str(e)}", exc_info=True)
            result.errors.append(str(e))
            raise

        return result.successful

    @sync_to_async
    def bulk_operations(self, model, records_to_insert, records_to_update, batch_size):
        """Perform bulk database operations with improved error handling."""
        with transaction.atomic():
            if records_to_insert:
                self.logger.info(f"Inserting {len(records_to_insert)} new records")
                model.objects.bulk_create(
                    records_to_insert,
                    batch_size=batch_size,
                    ignore_conflicts=True
                )

            if records_to_update:
                self.logger.info(f"Updating {len(records_to_update)} existing records")
                fields_to_update = list(self.get_model_fields(model))
                model.objects.bulk_update(
                    records_to_update,
                    fields=fields_to_update,
                    batch_size=batch_size
                )