# Зависимости
```
pip install -r requirements.txt
```

# Использование
- Запускать сервер с app.py после установки всех нужных библиотек
  
  ```
  python app.py
  ```
  Далее можно отправлять запросы на сервер
- Тестовые запросы и обработка ответа есть в requester.py, чтобы можно было быстро посмотреть взаимодействие с сервером.
  ```
  # При запущенном сервере данный запуск приведет к отправке запросов на оба типа конвертации с нужными файлами.
  # Возможно, придется поменять hostname у переменной url в requester.py. По умолчанию 127.0.0.1:5000
  python requester.py
  ```
- Запросы отправляются по URL с соответствующим Content-type: 
    1. URL для JSON->XML: "http://hostname/json_to_xml", Content-type: "application/json"

    ```
    url = "http://127.0.0.1:5000/json_to_xml"
    headers = {'Content-type': 'application/json'}
    with open("modules/templates/App_info.json", encoding="utf-8") as file:
        data = json.load(file)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    ```
    2. URL для XML->JSON: "http://hostname/xml_to_json", Content-type: "application/xml" (XML должен отправляться в UTF-8)

    ```
    url = "http://127.0.0.1:5000/xml_to_json"
    headers = {"Content-type": "application/xml"}
    with open("modules/templates/Get_Entrant_List.xml", encoding="utf-8") as file:
        data = file.read()
    response = requests.post(url, data=data.encode("utf-8"), headers=headers)
    ```
- Ответы сервера в случае удачной обработки:
    1. Для JSON->XML: в теле находится XML в кодировке UTF-8
    2. Для XML->JSON: в теле находится JSON
- Файл с настройками config.py, там можно включить/выключить валидацию XML
- По умолчанию включена валидация XML, поэтому в невалидных случаях сервер возвращает ошибку
    1. Get_Entrant_List.xml - пример валидного входа для xml->json
    2. App_info.json - пример валидного входа для json->xml

# Уточнения
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

6) Код классов в modules содержит комментарии, поясняющие их назначение
