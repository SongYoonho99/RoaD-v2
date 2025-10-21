'''핵심 함수 및 유틸 함수 모음 모듈'''
from tkinter import font
from io import BytesIO

from gtts import gTTS
from pygame import mixer

import api_client
from constants import Color, Text_D

# ==============================
# 유틸 함수
# ==============================
def internet_connected():
    '''인터넷 연결 확인'''
    try:
        tts = gTTS(text='test', lang='en')
        tts.save('nul')
        return True
    except:
        return False

def audio_connected():
    '''오디오 출력장치 연결 확인'''
    try:
        mixer.init()
        return True
    except:
        return False

def center_window(window, width, height):
    '''창을 화면 정중앙에 띄우는 함수'''
    x = window.winfo_screenwidth() // 2 - width // 2
    y = window.winfo_screenheight() // 2 - height // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def clear_placeholder(event):
    '''Username이 적혀 있는 엔트리창 클릭 시 플레이스 홀더 제거'''
    if event.widget.get() == 'Username':
        event.widget.delete(0, len(event.widget.get()))

def show_temporarymessage(message, text, color=Color.FONT_RED):
    '''메시지를 띄우고 4초후에 없애는 함수'''
    message.config(fg=color, text=text)
    message.after(4000, lambda: message.config(text = ''))

def limit_entry_length(entry, max_len=15):
    '''Entry에 입력 가능한 글자 수를 15자로 제한'''
    def on_validate(new_value):
        return len(new_value) <= max_len
    vcmd = (entry.register(on_validate), '%P')
    entry.config(validate='key', validatecommand=vcmd)

def type_writer(label, text, delay=50):
    '''Label의 글자를 한 글자씩 출력'''
    fnt = font.Font(font=label['font'])
    label.config(width=max(1, fnt.measure(text) // fnt.measure('e'))) # e 가 한글, 일본어 양쪽대응

    def inner(idx=0):
        if idx <= len(text):
            label.config(text=text[:idx])
            label.after(delay, inner, idx+1)
    inner()

def copy_word(obj, event):
    '''영단어 복사 후 복사이미지를 2초동안 체크이미지로 변경'''
    text_to_copy = obj.word_lbl.cget('text')
    obj.clipboard_clear()
    obj.clipboard_append(text_to_copy)
    event.widget.config(image=obj.controller.check_icon)
    event.widget.after(2000, lambda: event.widget.config(image=obj.controller.copy_icon))

def copy_dict(obj, event):
    '''사전 URL 복사 후 복사이미지를 2초동안 체크이미지로 변경'''
    text_to_copy = event.widget.cget('text')
    if ':' in text_to_copy:
        url = text_to_copy.split(':', 1)[1].strip()
    else:
        url = text_to_copy
    obj.clipboard_clear()
    obj.clipboard_append(url)
    event.widget.config(image=obj.controller.check_icon)
    event.widget.after(2000, lambda: event.widget.config(image=obj.controller.copy_icon))

def play_pronunciation(obj, word):
    '''영단어 발음 재생'''
    if obj.controller.audio:
        tts = gTTS(text=word, lang='en')
        mp3_crt = BytesIO()
        tts.write_to_fp(mp3_crt)
        mp3_crt.seek(0)
        mixer.music.load(mp3_crt, "mp3")
        mixer.music.play()

def on_mousewheel(event, canvas):
    '''마우스스크롤로 스크롤 가능하도록 하는 함수'''
    canvas.yview_scroll(-1 * (event.delta // 120), 'units')

def on_frame_configure(event, canvas):
    '''위젯의 크기, 위치, 또는 내부 구조가 변경될 때 스크롤영역 자동갱신'''
    canvas.configure(scrollregion=canvas.bbox('all'))

# ==============================
# api 호출 전후 처리 함수
# ==============================
def validate_login(obj, username):
    '''로그인시 등록된 유저인지 확인 및 언어, 단어개수, add여부, 단어 반환'''
    if not username or username == 'Username':
        show_temporarymessage(obj.message_lbl, 'Please enter ID')
        return
    
    response = api_client.login(obj, username)
    if response is None:
        return
    elif response.status_code == 400:
        show_temporarymessage(obj.message_lbl, 'ID not found')
    elif response.status_code == 201:  # 로그인 성공
        # DailyFrame의 위젯을 활성화하며 필요함수 전달
        addbool = response.json().get('category') == 'add_yourself'
        from ui import DailyFrame
        daily_frame = obj.controller.frames[DailyFrame]
        daily_frame.set_data(
            username,
            response.json().get('language'),
            response.json().get('dayword'),
            response.json().get('today_word'),
            addbool,
            response.json().get('check_streak')
        )
        obj.controller.show_frame(DailyFrame)
        daily_frame.create_widgets()
        # TODO: 오늘의 단어 선정하는 함수 호출해야함
        # TODO: check_streak이 -1일시 dailyFrame에 단어같은거 안띄워야함
    else:
        obj.controller.show_overframe('Instance Connection Failure')

def validate_signup(obj, username, language, dayword, category, errormessage, signup_window):
    '''회원가입 처리 함수'''
    # username 유효성 검사 (미작성 혹은 15자 초과일 경우)
    if not username or username == 'Username':
        show_temporarymessage(errormessage, 'Please enter username.')
        return
    if len(username) > 15:
        show_temporarymessage(errormessage, '15 characters max for username.')
        return

    # dayword 유효성 검사 (미작성 혹은 10 ~ 25사이의 자연수가 아닌 경우)
    try:
        dayword = int(dayword)
    except:
        show_temporarymessage(errormessage, 'Enter a number from 10 to 25.')
        return
    if not (10 <= dayword <= 25):
        show_temporarymessage(errormessage, 'Enter a number from 10 to 25.')
        return
    
    # 회원가입 api통신 전 데이터 가공
    language = 'K' if language == ' korean' else 'J'
    if category == ' add yourself':
        category = 'add_yourself'
    else:
        category = 'word_' + category.strip()

    # 회원가입 api통신함수 호출 (상태코드 201이 성공)
    response = api_client.signup(obj, username, language, dayword, category)
    if response is None:
        return
    elif response.status_code == 201:
        show_temporarymessage(obj.message_lbl, response.json().get('message'), Color.FONT_DEFAULT)
        signup_window.destroy()
    else:
        show_temporarymessage(errormessage, response.json().get('message'))

def delaccount_check_user(obj, username, errormessage, delaccount_window):
    '''계정 삭제시 등록된 유저인지 확인 (True, False)'''
    if api_client.delete_username_check(obj, username):
        obj.delaccount_reconfirm_window(username, delaccount_window)
    else:
        show_temporarymessage(errormessage, 'ID not found')

def validate_delaccount(obj, input, username, errormessage, delaccount_window):
    '''계정 삭제 처리 함수'''
    if input == f'delete {username}':
        response = api_client.delaccount(obj, username)
        if response is None:
            obj.controller.show_overframe('Instance Connection Failure')
        elif response.status_code == 200:
            show_temporarymessage(obj.message_lbl, response.json().get('message'), Color.FONT_DEFAULT)
            delaccount_window.destroy()
        else:
            show_temporarymessage(errormessage, response.json().get('message'))
    else:
        show_temporarymessage(errormessage, 'Incorrect input.')

# ==============================
# 프로그램 로직 함수
# ==============================
def streak_login(check_streak, language):
    '''최초로그인 or 연속로그인상태 or 오늘이미 완료 라벨 띄우는 함수'''
    if check_streak == -2:
        return Text_D.INITIAL_LOGIN[language]
    elif check_streak == -1:
        return Text_D.TODAY_DONE[language]
    elif check_streak == 0:
        return Text_D.STREAK_0[language]
    else:
        return f'{check_streak}{Text_D.STREAK[language]}'