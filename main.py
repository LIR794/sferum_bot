import datetime
import os
from dotenv import load_dotenv
from methods.match_module import get_schedule_changes
from methods.bells import get_bells_changes
from methods.send import send_main_sferum
from methods.send import send_all_sferum
from methods.send import send_test_sferum
from methods.send import send_bells_sferum
from methods.lin_auth_module import get_vk_token

date_now = datetime.datetime.now()

current_date = date_now.strftime('%d.%m.%Y')

tommorow = (date_now + datetime.timedelta(days=1)).strftime('%d.%m.%Y')

load_dotenv("/app/data/.env")

"""
Список id чатов:
    "РКЭ" = 
    "Test" = 2000000024
Для рассылки в несколько чатов, необходимо передать значения через запятую
"""

chats = os.getenv('chat_id')

today_groups_list = []
today_bells_list = []
today_type = 'сегодня'

tommorow_groups_list = []
tommorow_bells_list = []
tommorow_type = 'завтра'

message_status = []

# "TOKEN TEST"
send_all_sferum("test","2000000024",message_status)
print(message_status)

if 'response' not in message_status[0]:
    get_vk_token()
    send_test_sferum(f"{date_now.strftime('%H:%M:%S')}",chats,message_status)
    exit()

get_schedule_changes(current_date, today_groups_list)
get_schedule_changes(tommorow, tommorow_groups_list)

get_bells_changes(current_date, today_bells_list)
get_bells_changes(tommorow, tommorow_bells_list)

today_groups_list_str = ", ".join(today_groups_list)
tommorow_groups_list_str = ", ".join(tommorow_groups_list)

today_bells_list_str = ", ".join(today_bells_list)
tommorow_bells_list_str = ", ".join(tommorow_bells_list)

send_main_sferum(today_type,today_groups_list_str,chats,message_status)
send_main_sferum(tommorow_type,tommorow_groups_list_str,chats, message_status)

send_bells_sferum(today_type,today_bells_list_str,chats,message_status)
send_bells_sferum(tommorow_type,tommorow_bells_list_str,chats,message_status)
