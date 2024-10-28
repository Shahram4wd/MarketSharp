from data_import.models import CustomField
from data_import.base_processor import BaseProcessor, FieldMapping
from data_import.registry import ProcessorRegistry

def register_processor(registry: ProcessorRegistry):
    registry.register(
        endpoint='custom_fields',
        api_url='https://api4.marketsharpm.com/WcfDataService.svc/CustomFields',
        model=CustomField,
        processor_class=CustomFieldProcessor
    )

class CustomFieldProcessor(BaseProcessor):
    field_mappings = {
        'id': FieldMapping('id', 'id', 'uuid', required=True, is_primary_key=True),
        'name': FieldMapping('name', 'name', 'string'),
        'value': FieldMapping('value', 'value', 'string'),
        'contact_id': FieldMapping('contactId', 'contact_id', 'uuid'),
    }

    async def process_objects(self, xml_data: str, batch_size: int) -> int:
        """Process CustomField objects using shared logic in BaseProcessor."""
        entries = self.data_processor.parse_xml(xml_data)
        return await self.process_entries(entries, CustomField, self.field_mappings, batch_size)
