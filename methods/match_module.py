import requests
import json
import os

def get_schedule_changes(date, groups_to_send):
    
    current_date = date

    # Заголовки для запроса
    header = {
        "Accept": "application/json",
    }

    # Запрос данных расписания
    response = requests.get(f"https://апи.пары.ркэ.рф/api/schedules/public?date={current_date}", headers=header)

    if response.status_code != 200:
        print(f"Ошибка при загрузке данных: {response.status_code}")
        return

    data = response.json()

    group_data = {
        "last_updated": data['last_updated'],
        "schedules": []
    }

    # Проверка наличия файла с предыдущими данными
    if not os.path.isfile(f"/app/data/changes/{current_date}.json"):
        for schedule in data['schedules']:
            group_name = schedule['group_name']
            schedule_type = schedule['type']
            schedule_data = schedule['lessons']

            if schedule_type == 'changes':
                schedule_entry = {
                    group_name: schedule_data
                }
                group_data["schedules"].append(schedule_entry)

                # Сохраняем новые данные в файл с текущей датой
                with open(f'/app/data/changes/{current_date}.json', 'w', encoding='utf-8') as file:
                    json.dump(group_data, file, ensure_ascii=False)

                # Добавляем группу в список изменений
                groups_to_send.append(group_name)
        return

    # Если файл существует, загружаем предыдущие данные
    with open(f"/app/data/changes/{current_date}.json", encoding="utf-8") as f:
        file_data = json.load(f)

    # Проверяем, обновились ли данные
    if data['last_updated'] != file_data['last_updated']:
        print("Данные обновились, сравниваем расписания.")
        for schedule in data['schedules']:
            group_name = schedule['group_name']
            schedule_type = schedule['type']
            schedule_data = schedule['lessons']

            # Проверка на тип 'changes'
            if schedule_type == 'changes':
                file_schedule_entry = next((sch for sch in file_data['schedules'] if group_name in sch), None)

                if not file_schedule_entry:
                    # Группа не найдена в файле, добавляем новую
                    file_data['schedules'].append({group_name: schedule_data})
                    groups_to_send.append(group_name)
                else:
                    # Группа найдена, проверяем совпадают ли расписания
                    if file_schedule_entry[group_name] != schedule_data:
                        # Обновляем расписание и добавляем в список для отправки
                        file_schedule_entry[group_name] = schedule_data
                        groups_to_send.append(group_name)

            # Проверка на тип 'main'
            elif schedule_type == 'main':
                file_schedule_entry = next((sch for sch in file_data['schedules'] if group_name in sch), None)

                if file_schedule_entry:
                    # Обновляем уроки на новые данные
                    file_schedule_entry[group_name] = schedule_data
                    groups_to_send.append(group_name)  # Добавляем группу в список изменений

        # Обновляем group_data с данными file_data после всех изменений
        group_data['schedules'] = file_data['schedules']

        # Сохраняем новые данные в файл с текущей датой
        with open(f'/app/data/changes/{current_date}.json', 'w', encoding='utf-8') as file:
            json.dump(group_data, file, ensure_ascii=False)