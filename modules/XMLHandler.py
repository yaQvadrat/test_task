import xmltodict
from typing import Any
from modules.Constants import KEY_MAP


SPECIAL_CASES = ("Address", "Document")


class XMLHandler:
    """
    Класс для обработки словаря для создания словаря по образцу
    App_info.json из исходной XML строки, созданной на основе Get_Entrant_List.xsd.

    Поля:
    - __xml_data: dict
    Входной XML в виде словаря.
    """

    def __init__(self, xml: str) -> None:
        """
        Инициализация __xml_data с парсингом входной строки в словарь при помощи библиотеки.

        Параметры:
        - xml: str
        Исходная XML строка.
        """

        self.__xml_data = xmltodict.parse(xml)
    
    def handle_data(self) -> dict[str, Any]:
        """
        Обработка __xml_data, которая заполняет пустой словарь по образцу.

        Возвращает:
        - Заполненный словарь
        """

        return self.__parse({}, self.__xml_data)
    
    def __parse(self, to_fill: dict, source: dict[str, Any]) -> dict[str, Any]:
        """
        Рекурсивный обход всего источника с заполнением словаря.

        Параметры:
        - to_fill: dict
        Заполняемый словарь.
        - source: dict[str, Any]
        Словарь, полученнный из XML и являющийся источником данных.
        Возвращает:
        - Заполненный словарь
        """

        for key in source:
            if key in SPECIAL_CASES:
                self.__resolve_special_cases(key, to_fill, source)
                continue
            if isinstance(source[key], dict):
                self.__parse(to_fill, source[key])
                continue
            real_key = KEY_MAP[key] if key in KEY_MAP else key.lower()
            to_fill[real_key] = source[key]

        return to_fill
    
    def __resolve_special_cases(self, key: str, to_fill: dict, source: dict[str, Any]) -> None:
        """
        Отдельный парсер особенных случаев/полей, для которых нужен отдельный алгоритм заполнения.

        Параметры:
        - key: str
        Ключ, который является особенным.
        - to_fill: dict
        Заполняемый словарь.
        - source: dict[str, Any]
        Словарь, полученнный из XML и являющийся источником данных.
        """

        match key:
            case "Address":
                addresses = source[key]
                digit = {"true": "1", "false": "2"}
                for address in addresses:
                    for field in address:
                        real_key = KEY_MAP[field] if field in KEY_MAP else field.lower()
                        to_fill[real_key + digit[address["IsRegistration"]]] = address[field] 
            case "Document":
                documents = source[key]
                digit = "1"
                for doc in documents:
                    for field in doc:
                        real_key = KEY_MAP[field] if field in KEY_MAP else field.lower()
                        to_fill[real_key + digit] = doc[field] 
                    digit = str(int(digit) + 1)
