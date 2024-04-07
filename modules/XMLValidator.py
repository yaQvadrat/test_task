import xmlschema


class XMLValidator:
    """
    Класс для валидации XML по заданной XSD-схеме.

    Поля:
    - __schema: XMLSchema объект
    Используется для применения метода валидации из библиотеки.
    """

    def __init__(self, xsd_path: str) -> None:
        """
        Инициализация класса с путем к XSD-схеме.

        Параметры:
        - xsd_path: str
        Путь к XSD-схеме для валидации XML.
        """

        self.__schema = xmlschema.XMLSchema(xsd_path)
        
    def validate_xml_string(self, xml: str) -> bool:
        """
        Валидация XML-строки по заданной XSD-схеме.

        Параметры:
        - xml: str
        Строка XML для валидации.

        Возвращает:
        - True, если XML валиден, иначе False.
        """

        try:
            self.__schema.validate(xml)
            return True
        except xmlschema.XMLSchemaValidationError as ex:
            return False
    
    def validate_xml_file(self, xml_path: str) -> bool:
        """
        Валидация XML-файла по заданной XSD-схеме.

        Параметры:
        - xml_path: str
        Путь к XML-файлу для валидации.

        Возвращает:
        - True, если XML валиден, иначе False.
        """
        
        try:
            self.__schema.validate(xml_path)
            return True
        except xmlschema.XMLSchemaValidationError as ex:
            return False
