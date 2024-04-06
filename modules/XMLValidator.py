import xmlschema


class XMLValidator:
    def __init__(self, xsd_path: str) -> None:
        self.__schema = xmlschema.XMLSchema(xsd_path)
        
    def validate_xml_string(self, xml: str) -> bool:
        try:
            self.__schema.validate(xml)
            return True
        except xmlschema.XMLSchemaValidationError as ex:
            return False
    
    def validate_xml_file(self, xml_path: str) -> bool:
        try:
            self.__schema.validate(xml_path)
            return True
        except xmlschema.XMLSchemaValidationError as ex:
            return False
