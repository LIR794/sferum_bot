import requests
import os
import random
from dotenv import load_dotenv

def send_main_sferum (date_type, groups, chats_id, status):
    
        if not groups:
            print("Изменений в группах нет")
            return
    
        load_dotenv()

        token = os.getenv('token')

        peer_id = f'{chats_id}'
        
        message = f'ВНИМАНИЕ! Изменилось расписание на {date_type} по группам: {groups}. Просьба к классным руководителям оповестить своих студентов'
        
        url = 'https://api.vk.com/method/messages.send'

        data = {
            'access_token': token,
            'peer_id': peer_id,
            'random_id' : (random.randint(0, 999999)),
            'message' : message,
            'group_id': 0,
        }
        params = {
            'v': 5.241
        }
    
        response = requests.post(url, data=data, params=params)
        msg = response.json()
        status.append(msg)

def send_test_sferum (time, chats_id, status):
    
        load_dotenv()

        token = os.getenv('token')

        peer_id = f'{chats_id}'
        
        message = f'Токен просрочен, запрос на получение нового : {time}'
        
        url = 'https://api.vk.com/method/messages.send'

        data = {
            'access_token': token,
            'peer_id': peer_id,
            'random_id' : (random.randint(0, 999999)),
            'message' : message,
            'group_id': 0,
        }
        params = {
            'v': 5.241
        }
    
        response = requests.post(url, data=data, params=params)
        msg = response.json()
        
        status.append(msg)

def send_all_sferum (message,chats_id,status):
    
        load_dotenv()

        token = os.getenv('token')

        peer_id = f'{chats_id}'
        
        message = f'{message}'
        
        url = 'https://api.vk.com/method/messages.send'

        data = {
            'access_token': token,
            'peer_id': peer_id,
            'random_id' : (random.randint(0, 999999)),
            'message' : message,
            'group_id': 0,
        }
        params = {
            'v': 5.241
        }
    
        response = requests.post(url, data=data, params=params)
        msg = response.json()
        
        status.append(msg)
