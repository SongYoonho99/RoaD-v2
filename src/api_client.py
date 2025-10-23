'''EC2인스턴스의 API 서버와 연결을 담당하는 모듈'''
import os

import requests
from dotenv import load_dotenv

# EC2 인스턴스 서버의 기본 주소
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
EC2_IP = os.getenv('EC2_IP')
base_URL = f'http://{EC2_IP}:5000/'

def server_check(obj):
    '''프로그램 시작 시 서버 작동여부와 데이터베이스상태 확인'''
    try:
        URL = f'{base_URL}server_check'
        response = requests.get(URL)

        if response.status_code != 200:
            obj.show_overframe(response.json().get('message'))
            return False
    except:
        obj.show_overframe('Instance Connection Failure')
        return False
    
    return True

def login(obj, username):
    '''로그인 처리 함수'''
    payload = {'username': username}
    try:
        URL = f'{base_URL}login'
        response = requests.post(URL, json=payload)
        return response
    except:
        obj.controller.show_overframe(response.json().get('message'))

def take_more_word(obj):
    payload = {'username': obj.username, 'n': len(obj.today_word) + obj.dayword - len(obj.today_confirm)}
    try:
        URL = f'{base_URL}take_more_word'
        response = requests.post(URL, json=payload)
        return response
    except:
        obj.controller.show_overframe('Instance Connection Failure')
        return

def take_category(obj):
    '''단어 카테고리명을 반환하는 함수'''
    try:
        URL = f'{base_URL}take_category'
        response = requests.get(URL)

        if response.status_code == 200:
            tables = response.json().get('word_tables')
            table_name = [f" {t[5:]}" for t in tables]
            return table_name
        else:
            obj.controller.show_overframe(response.json().get('message'))
            return []
    except:
        obj.controller.show_overframe('Instance Connection Failure')
        return []
    
def signup(obj, username, language, dayword, category):
    '''회원가입을 처리하는 함수'''
    payload = {
        'username': username, 'language': language, 'dayword': dayword, 'category': category
    }
    try:
        URL = f'{base_URL}signup'
        response = requests.post(URL, json=payload)
        return response
    except:
        obj.controller.show_overframe('Instance Connection Failure')

def delete_username_check(obj, username):
    '''username이 존재하는지 확인하는 함수'''
    payload = {'username': username}
    try:
        URL = f'{base_URL}delete_username_check'
        response = requests.post(URL, json=payload)

        if response.status_code == 200:
            return response.json().get('message')
        else:
            obj.controller.show_overframe(response.json().get('message'))
    except:
        obj.controller.show_overframe('Instance Connection Failure')

def delaccount(obj, username):
    '''계정 삭제를 처리하는 함수'''
    payload = {'username': username}
    try:
        URL = f'{base_URL}delaccount'
        response = requests.delete(URL, json=payload)
        return response
    except:
        obj.controller.show_overframe('Instance Connection Failure')