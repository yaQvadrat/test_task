import xmltodict
from typing import Any
from modules.Constants import KEY_MAP


SPECIAL_CASES = ("Address", "Document")


class XMLHandler:
    def __init__(self, xml: str) -> None:
        self.__xml_data = xmltodict.parse(xml)
    
    def handle_data(self) -> dict[str, Any]:
        return self.__parse({}, self.__xml_data)
    
    def __parse(self, to_fill: dict, source: dict[str, Any]) -> dict[str, Any]:
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
