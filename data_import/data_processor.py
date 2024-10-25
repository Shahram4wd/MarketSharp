import re
import lxml.etree as ET
from data_import.marketsharp_api import MarketSharpAPI
from functools import cached_property

class DataProcessor:
    def __init__(self, logger):
        self.logger = logger

    @cached_property
    def nsmap(self):
        return {
            'atom': 'http://www.w3.org/2005/Atom',
            'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices',
            'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'
        }

    def sanitize_xml(self, xml_data):
        """Sanitize XML data by removing invalid characters."""
        if not isinstance(xml_data, str):
            raise TypeError(f"Expected string for XML data but got {type(xml_data)}")

        # Remove null bytes and specific invalid character references
        xml_data = xml_data.replace('\x00', '')
        xml_data = re.sub(r'&#x[0-9A-Fa-f]+;', '', xml_data)

        # Regular expression to remove other invalid XML characters
        invalid_xml_char_pattern = re.compile(
            r'[\x01-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F\uFDD0-\uFDEF\uFFFE\uFFFF]|'
            r'[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]'
        )
        # Substitute invalid characters with an empty string
        return invalid_xml_char_pattern.sub('', xml_data)

    def parse_xml(self, xml_data):
        """Parse XML and return root entries."""
        # Sanitize XML before parsing to ensure no invalid characters remain
        sanitized_xml_data = self.sanitize_xml(xml_data)
        try:
            root = ET.fromstring(sanitized_xml_data.encode('utf-8'))
            return root.findall('.//atom:entry', namespaces=self.nsmap)
        except ET.XMLSyntaxError as e:
            self.logger.error(f"Error parsing XML: {e}")
            raise

    def get_xml_text(self, parent, tag_name):
        """Helper function to extract text from XML elements."""
        element = parent.find(f'd:{tag_name}', namespaces=self.nsmap)
        if element is not None and element.get('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}null') != 'true':
            return element.text
        return None

    def get_xml_bool(self, value: str) -> bool:
        """Helper function to convert string value to boolean."""
        return value.lower() == 'true' if value else False

    def get_xml_float(self, parent, tag_name):
        """Helper function to extract float values from XML elements."""
        text_value = self.get_xml_text(parent, tag_name)
        try:
            return float(text_value) if text_value else None
        except ValueError:
            self.logger.warning(f"Could not convert '{text_value}' to float for tag '{tag_name}'")
            return None
