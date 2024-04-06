pip install flask
pip install xmltodict
pip install xmlschema
pip install requests

1) Добавил в JSON поля для FreeEducationReason (free_education_reason_id).
Данный элемент заполняется только в случае, когда "is_foreigner": true

2) Добавил в JSON full_addr1, city1, region_id1, full_addr2, city2, region_id2 для удобства парсинга. 
Первый адрес - всегда IsRegistration: true, наличие второго определяется по
has_another_living_address

3) Поменял в JSON для прохождения проверки: форматы у дат, снилс.
Если убрать изменения и оставить включенной валидацию, то будет в ответ будет возвращаться ошибка (418),
так как изначальные входные данные были невалидны по типам из xsd.

4) Остальные сопоставления ключей проводились либо переводом в ловеркейс, либо использовался
вручную составленный словарь в Constants.py

5) Опциональная валидация входного XML при конвертации XML->JSON работает тем же образом как при 
JSON->XML, то есть при невалидном XML возвращается ошибка (418)

6) XML->JSON ожидает Content-Type application/xml
