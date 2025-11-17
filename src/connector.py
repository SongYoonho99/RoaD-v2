'''EC2인스턴스의 API 서버와 연결을 담당하는 모듈'''
import os

import requests

from logic import show_temp_message, start_test
from constants import Color

def load_ec2_ip():
    global EC2_IP
    global base_URL
    
    EC2_IP = os.getenv('EC2_IP')
    base_URL = f'http://{EC2_IP}:5000/'

def _request_wrapper(method, url, json=None):
    try:
        if method == 'get':
            return requests.get(url)
        elif method == 'post':
            return requests.post(url, json=json)
        elif method == 'put':
            return requests.put(url, json=json)
        elif method == 'delete':
            return requests.delete(url, json=json)
    except Exception as e:
        print(e)
        return

# ==============================
# check server and db
# ==============================
def _check_server_and_db():
    URL = f'{base_URL}check_server_and_db'
    return _request_wrapper('get', URL)
    
def check_server_and_db(obj):
    response = _check_server_and_db()
    if response is None:
        obj.show_overlay('Instance connection failure.')
        return False
    elif response.status_code == 200:
        return True
    else:
        obj.show_overlay(response.json().get('message'))
        return False

# ==============================
# take category
# ==============================
def _take_category():
    URL = f'{base_URL}take_category'
    return _request_wrapper('get', URL)

def take_category(obj):
    response = _take_category()
    if response is None:
        obj.controller.show_overlay('Instance connection failure.')
        return False
    elif response.status_code == 200:
        word_tables = response.json().get('word_tables')
        category = [f' {t[5:]}' for t in word_tables]
        return category
    else:
        obj.controller.show_overlay(response.json().get('message'))
        return False

# ==============================
# sign up
# ==============================
def _sign_up(payload):
    URL = f'{base_URL}sign_up'
    return _request_wrapper('post', URL, payload)

def sign_up(obj, username, language, dayword, category, errormessage, sign_up_window):
    # username 유효성 검사 (미작성 시)
    if not username or username == 'Username':
        show_temp_message(errormessage, 'Please enter username.')
        return

    # dayword 유효성 검사 (미작성 혹은 10 ~ 25사이의 자연수가 아닐 시)
    try:
        dayword = int(dayword)
    except:
        show_temp_message(errormessage, 'Enter a number from 10 to 25.')
        return
    if not (10 <= dayword <= 25):
        show_temp_message(errormessage, 'Enter a number from 10 to 25.')
        return
    
    # 회원가입 api통신 전 데이터 가공
    language = 'K' if language == ' korean' else 'J'
    if category == ' add yourself':
        category = category.strip()
    else:
        category = 'word_' + category.strip()

    payload = {
        'username': username, 'language': language, 'dayword': dayword, 'category': category
    }
    response = _sign_up(payload)
    if response is None:
        obj.controller.show_overlay('Instance connection failure.')
        sign_up_window.destroy()
    elif response.status_code == 201:
        show_temp_message(obj.message_lbl, response.json().get('message'), Color.FONT_DEFAULT)
        sign_up_window.destroy()
    elif response.status_code == 400:
        show_temp_message(errormessage, response.json().get('message'))
    else:
        obj.controller.show_overlay(response.json().get('message'))
        sign_up_window.destroy()

# ==============================
# check user before delete
# ==============================
def _check_user_before_delete(payload):
    URL = f'{base_URL}check_user_before_delete'
    return _request_wrapper('post', URL, payload)

def check_user_before_delete(obj, username, errormessage, delete_account_window):
    payload = {'username': username}
    response = _check_user_before_delete(payload)
    if response is None:
        obj.controller.show_overlay('Instance connection failure.')
        delete_account_window.destroy()
    elif response.status_code == 200 and response.json().get('message'):
        obj.open_reconfirm_window(username, delete_account_window)
    elif response.status_code == 200 and not response.json().get('message'):
        show_temp_message(errormessage, 'ID not found')
    else:
        obj.controller.show_overlay(response.json().get('message'))
        delete_account_window.destroy()

# ==============================
# delete account
# ==============================
def _delete_account(payload):
    URL = f'{base_URL}delete_account'
    return _request_wrapper('delete', URL, payload)

def delete_account(obj, input, username, errormessage, delete_account_window):
    if input != f'delete {username}':
        show_temp_message(errormessage, 'Incorrect input')
        return

    payload = {'username': username}
    response = _delete_account(payload)
    if response is None:
        obj.controller.show_overlay('Instance connection failure.')
        delete_account_window.destroy()
    elif response.status_code == 200:
        show_temp_message(obj.message_lbl, response.json().get('message'), Color.FONT_DEFAULT)
        delete_account_window.destroy()
    elif response.status_code == 400:
        show_temp_message(errormessage, response.json().get('message'))
    else:
        obj.controller.show_overlay(response.json().get('message'))
        delete_account_window.destroy()

# ==============================
# login
# ==============================
def _login(payload):
    URL = f'{base_URL}login'
    return _request_wrapper('post', URL, payload)

def login(obj, username):
    if not username or username == 'Username':
        show_temp_message(obj.message_lbl, 'Please enter ID')
        return
    
    payload = {'username': username}
    response = _login(payload)
    if response is None:
        obj.controller.show_overlay('Instance connection failure.')
    elif response.status_code == 201:
        language = response.json().get('language')
        dayword = response.json().get('dayword')
        is_add_yourself = response.json().get('category') == 'add yourself'
        today_word = response.json().get('today_word')
        streak = response.json().get('streak')

        # 오늘의 단어로 추가할 항목이 없고, add yourself가 아닐때 TODO:
        if not today_word and not is_add_yourself:
            start_test(obj, username, language, is_add_yourself, streak, is_exist_today_word = False)
            return

        # 로그인 성공
        daily_frm = obj.controller.frames['DailyFrame']
        daily_frm.init_data(username, language, dayword, today_word, is_add_yourself, streak)
        daily_frm.create_widgets()
        obj.controller.show_frame('DailyFrame')
        if not streak and not is_add_yourself:
            daily_frm.open_manual_window()
        if not streak == -2 and is_add_yourself:
            daily_frm.open_add_yourself_manual_window()

    elif response.status_code == 204:
        # TODO: 모든 단어가 status == finish 일때
        pass
    elif response.status_code == 400:
        show_temp_message(obj.message_lbl, response.json().get('message'))
    else:
        obj.controller.show_overlay(response.json().get('message'))

# ==============================
# take more word
# ==============================
def _take_more_word(payload):
    URL = f'{base_URL}take_more_word'
    return _request_wrapper('post', URL, payload)

def take_more_word(obj, message_lbl):
    payload = {
        'username': obj.username,
        'today_word': obj.today_word,
        'necessary': obj.dayword - len(obj.today_confirm)
    }
    response = _take_more_word(payload)
    if response is None:
        obj.controller.show_overlay('Instance connection failure.')
        return False
    elif response.status_code == 200:
        return response.json().get('added_word')
    elif response.status_code == 400:
        show_temp_message(message_lbl, response.json().get('message'))
        return False
    else:
        obj.controller.show_overlay(response.json().get('message'))
        return False
    
# ==============================
# write today word
# ==============================
def _write_today_word(payload):
    URL = f'{base_URL}write_today_word'
    return _request_wrapper('post', URL, payload)

def write_today_word(obj):
    payload = {
        'username': obj.username,
        'today_confirm': obj.today_confirm,
        'already_know': obj.already_know,
        'is_add_yourself': obj.is_add_yourself
    }
    response = _write_today_word(payload)
    if response is None:
        obj.controller.show_overlay('Instance connection failure.')
        return False
    elif response.status_code == 201:
        return True
    else:
        obj.controller.show_overlay(response.json().get('message'))
        return False
    
# ==============================
# get test data
# ==============================
def _get_test_data(payload):
    URL = f'{base_URL}get_test_data'
    return _request_wrapper('post', URL, payload)

def get_test_data(obj, username):
    payload = {'username': username}
    response = _get_test_data(payload)
    if response is None:
        obj.controller.show_overlay('Instance connection failure.')
        return False
    elif response.status_code == 200:
        return response.json()
    else:
        obj.controller.show_overlay(response.json().get('message'))
        return False
    
# ==============================
# set retry word
# ==============================
def _set_retry_word(payload):
    URL = f'{base_URL}set_retry_word'
    return _request_wrapper('post', URL, payload)

def set_retry_word(obj):
    payload = {'username': obj.username, 'retry_word_list': obj.retry_word_list}
    response = _set_retry_word(payload)
    if response is None:
        obj.controller.show_overlay('Instance connection failure.')
    elif response.status_code == 200:
        obj.winfo_toplevel().destroy()
    else:
        obj.controller.show_overlay(response.json().get('message'))