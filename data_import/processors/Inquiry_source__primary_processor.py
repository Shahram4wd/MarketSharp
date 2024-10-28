from data_import.models import InquirySourcePrimary
from data_import.base_processor import BaseProcessor, FieldMapping
from data_import.registry import ProcessorRegistry

def register_processor(registry: ProcessorRegistry):
    registry.register(
        endpoint='inquiry_source_primaries',
        api_url='https://api4.marketsharpm.com/WcfDataService.svc/InquirySourcePrimaries',
        model=InquirySourcePrimary,
        processor_class=InquirySourcePrimaryProcessor
    )

class InquirySourcePrimaryProcessor(BaseProcessor):
    field_mappings = {
        'id': FieldMapping('id', 'id', 'uuid', required=True, is_primary_key=True),
        'name': FieldMapping('name', 'name', 'string'),
        'is_active': FieldMapping('isActive', 'is_active', 'boolean', default=True),
        'company_id': FieldMapping('companyId', 'company_id', 'int'),
    }

    async def process_objects(self, xml_data: str, batch_size: int) -> int:
        """Process InquirySourcePrimary objects using shared logic in BaseProcessor."""
        entries = self.data_processor.parse_xml(xml_data)
        return await self.process_entries(entries, InquirySourcePrimary, self.field_mappings, batch_size)
