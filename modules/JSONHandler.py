import xmltodict
import json
from copy import deepcopy
from typing import Any
from modules.Constants import KEY_MAP, DOC_ID_OFFSET


with open("modules/templates/Add_Entrant_List.xml", encoding="utf-8") as file:
    PATTERN = xmltodict.parse(file.read())
with open("modules/templates/dict_document_type_cls.json", encoding="utf-8") as file:
    DOC_INFO = json.load(file)
SPECIAL_CASES = ("DocName", "Fields", "Address", "FreeEducationReason")


class JSONHandler:
    def __init__(self, raw_data: dict[str, Any]) -> None:
        self.__raw_data = deepcopy(raw_data)
    
    def handle_data(self, ret_XML: bool = False) -> dict[str, Any] | str:
        res = self.__parse({}, PATTERN)
        return xmltodict.unparse(res, pretty=True) if ret_XML else res 
    
    def __parse(self, to_fill: dict, pattern: dict[str, Any]) -> dict[str, Any]:
        for key in pattern:
            if key in SPECIAL_CASES:
                self.__resolve_special_cases(key, to_fill, pattern)
                continue
            if isinstance(pattern[key], dict):
                to_fill[key] = self.__parse({}, pattern[key])
                continue
            real_key = key.lower() if key.lower() in self.__raw_data else KEY_MAP[key]
            to_fill[key] = self.__raw_data.get(real_key, None)

        return to_fill
            
    def __resolve_special_cases(self, key: str, to_fill: dict, pattern: dict[str, Any]) -> None:
        match key:
            case "DocName":
                doc_id = self.__raw_data["passport_type_id"] + DOC_ID_OFFSET
                for doc in DOC_INFO:
                    if doc["Id"] == doc_id:
                        to_fill[key] = doc["Name"]
                        break
            case "FreeEducationReason":
                if self.__raw_data["is_foreigner"]:
                    to_fill[key] = {}
                    for i in pattern[key]:
                        to_fill[key][i] = self.__raw_data[KEY_MAP[i]]
            case "Fields":
                self.__fill_fields(to_fill)
            case "Address":
                self.__fill_address(to_fill, pattern)

    def __fill_fields(self, to_fill: dict) -> None:
        to_fill["Fields"] = {}
        doc_id = self.__raw_data["passport_type_id"] + DOC_ID_OFFSET
        doc = None
        for element in DOC_INFO:
            if element["Id"] == doc_id:
                doc = element
                break

        for field in doc["FieldsDescription"]["fields"]:
            name = field["xml_name"]
            to_fill["Fields"][name] = self.__raw_data[KEY_MAP[name]]

    def __fill_address(self, to_fill: dict, pattern: dict[str, Any]) -> None:
        to_fill["Address"] = [{}]
        self.__process_address("1", True, to_fill["Address"][0], pattern["Address"][0])
        if self.__raw_data["has_another_living_address"]:
            to_fill["Address"].append({})
            self.__process_address("2", False, to_fill["Address"][1], pattern["Address"][0])
        
    def __process_address(self, n: str, is_reg: bool, to_fill: dict, pattern: dict[str, Any]) -> None:
        for field in pattern:
            if field == "IsRegistration":
                to_fill[field] = is_reg
            else:
                to_fill[field] = self.__raw_data[KEY_MAP[field]+n]
