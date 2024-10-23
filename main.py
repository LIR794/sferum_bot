import datetime
from methods.match_module import get_schedule_changes
from methods.send import send_main_sferum
from methods.send import send_all_sferum
from methods.send import send_test_sferum
from methods.auth_module import get_vk_token

date_now = datetime.datetime.now()

current_date = date_now.strftime('%d.%m.%Y')

tommorow = (date_now + datetime.timedelta(days=1)).strftime('%d.%m.%Y')

"""
Список id чатов:
    "РКЭ" = 
    "Test" = 2000000023
Для рассылки в несколько чатов, необходимо передать значения через запятую
"""

chats = "2000000024"

today_list = []
today_type = 'сегодня'

tommorow_list = []
tommorow_type = 'завтра'

message_status = []

# "TOKEN TEST"
send_all_sferum("test",chats,message_status)
print(message_status)

if 'response' not in message_status[0]:
    get_vk_token()
    send_test_sferum(f"{date_now.strftime('%H:%M:%S')}",chats,message_status)
    exit()

get_schedule_changes(current_date, today_list)
get_schedule_changes(tommorow, tommorow_list)

today_list_str = ", ".join(today_list)
tommorow_list_str = ", ".join(tommorow_list)

send_main_sferum(today_type,today_list_str,chats,message_status)
send_main_sferum(tommorow_type,tommorow_list_str,chats, message_status)
