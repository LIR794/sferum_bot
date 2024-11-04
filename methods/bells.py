import requests
import json
import os

def get_bells_changes(current_date, builings_to_send):

    bells_data = {}

    header = {
        "Accept": "application/json",
    }

    response = requests.get(f"https://пары.ркэ.рф/api/bells/public?date={current_date}", headers=header)

    if response.status_code != 200:
        print(f"Ошибка при загрузке данных: {response.status_code}")
        return

    data = response.json()

    # Проверка наличия файла с предыдущими данными
    if not os.path.isfile(f"/app/data/changes/bells - {current_date}.json"):
        for dicts in data:
            bells_type = dicts["type"]
            bells_building = dicts["building"]
            if dicts["type"] == "changes":
                new_format = {
                    bells_building : bells_type
                }
                
                bells_data.update(new_format)

                builings_to_send.append(dicts["building"])
        
        with open(f'/app/data/changes/bells - {current_date}.json', 'w', encoding='utf-8') as file:
            json.dump(bells_data, file, ensure_ascii=False)
        
        return
    
    with open(f"/app/data/changes/bells - {current_date}.json", encoding="utf-8") as f:
        file_data = json.load(f)

    for dicts in data:
        bells_building = dicts["building"]
        bells_type = dicts["type"]
        
        if bells_building in file_data:
            if bells_type != file_data[bells_building]:
                del file_data[bells_building]
                builings_to_send.append(bells_building)
        
        else:
            if bells_type == "changes":

                new_format = {
                    bells_building : bells_type
                }
                
                file_data.update(new_format)
            
                builings_to_send.append(bells_building)


    with open(f'/app/data/changes/bells - {current_date}.json', 'w', encoding='utf-8') as file:
        json.dump(file_data, file, ensure_ascii=False)                