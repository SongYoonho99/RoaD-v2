'''핵심 함수 및 유틸 함수 모음 모듈'''
import random
import tkinter as tk
from tkinter import font
from io import BytesIO

from gtts import gTTS
from pygame import mixer

import api_client
from constants import Color, Font_E, Text_D, Tip

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

def audio_close(obj):
    '''프로그램 종료시 연결된 오디오를 종료'''
    if obj.audio:
        mixer.quit()
    obj.root.destroy()

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

def show_random_tip(obj, tip_lbl):
    '''TIP_D 또는 TIP_B로 시작하는 항목 중 하나를 랜덤 출력'''
    tip_attrs = [
        v for k, v in Tip.__dict__.items()
        if (k.startswith('TIP_D') or k.startswith('TIP_B')) and isinstance(v, dict)
    ]
    tip = random.choice(tip_attrs)
    tip_lbl.config(text=tip[obj.language])

def insert_word_lbl_list(obj, record_frm):
    '''오늘의 단어 추가화면 오른쪽 리스트에 단어 추가하는 함수'''
    lbl = tk.Label(
        record_frm, bg=Color.DEEP, fg=Color.FONT_DEFAULT, font=Font_E.SMALL, anchor='w',
        highlightthickness=5, highlightbackground = Color.DEEP, 
        text=f'{obj.pointer + 1}. {obj.today_word[obj.pointer][1]}'
    )
    lbl.pack(padx=(4, 0), fill='x')
    lbl.bind('<Button-1>', lambda e, idx=len(obj.word_lbl_list): word_lbl_click(obj, idx))
    obj.word_lbl_list.append(lbl)
    record_frm.update_idletasks()
    record_frm.master.yview_moveto(1.0)

def insert_word_lbl_list_addbool(obj, record_frm):
    '''오늘의 단어 추가화면 오른쪽 리스트에 단어 추가하는 함수(add yourself일때)'''
    lbl = tk.Label(
        record_frm, bg=Color.DEEP, fg=Color.FONT_DEFAULT, font=Font_E.SMALL, anchor='w',
        highlightthickness=5, highlightbackground = Color.DEEP, text=f'{obj.pointer + 1}. '
    )
    lbl.pack(padx=(4, 0), fill='x')
    lbl.bind('<Button-1>', lambda e, idx=len(obj.word_lbl_list): word_lbl_click(obj, idx))
    obj.word_lbl_list.append(lbl)
    record_frm.update_idletasks()
    record_frm.master.yview_moveto(1.0)

    # Entry 입력 감지
    text_var = tk.StringVar()
    obj.word_ent.config(textvariable=text_var)

    def sync_label(*_):
        obj.word_lbl_list[obj.pointer].config(text=f'{obj.pointer + 1}. {text_var.get()}')

    text_var.trace_add('write', sync_label)


def selected_scroll_widget(obj):
    '''pointer가 가르키는 스크롤바 내 라벨색상을 DAKR, 그 외에는 DEEP'''
    for idx, lbl in enumerate(obj.word_lbl_list):
        if idx == obj.pointer:
            lbl.config(bg=Color.DARK, highlightbackground=Color.DARK)
        else:
            lbl.config(bg=Color.DEEP, highlightbackground=Color.DEEP)

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
        # 로그인 성공 시 데이터 취득
        language = response.json().get('language')
        dayword = response.json().get('dayword')
        today_word = response.json().get('today_word')
        addbool = response.json().get('category') == 'add_yourself'
        streak = response.json().get('streak')

        # 오늘의 단어로 추가할 항목이 없고, add yourself가 아닐때
        if not today_word and not addbool:
            # TODO: 바로 테스트프레임으로 이동
            pass
        else:
            # DailyFrame의 위젯을 활성화하며 필요함수 전달
            from ui import DailyFrame
            daily_frame = obj.controller.frames[DailyFrame]
            daily_frame.set_data(username, language, dayword, today_word, addbool, streak)
            daily_frame.create_widgets()
            obj.controller.show_frame(DailyFrame)
            # 최초 로그인일 경우 설명서 윈도우 띄움
            if streak == -2 and not addbool:
                daily_frame.manual_window()
            if streak == -2 and addbool:
                daily_frame.addyourself_manual_window()

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
def streak(check_streak, language):
    '''최초로그인 or 연속로그인상태 or 오늘이미 완료 라벨 띄우는 함수'''
    if check_streak == -2:
        return Text_D.INITIAL_LOGIN[language]
    elif check_streak == -1:
        return Text_D.TODAY_DONE[language]
    elif check_streak == 0:
        return Text_D.STREAK_0[language]
    else:
        return f'{check_streak}{Text_D.STREAK[language]}'
    
def daily_confirm(obj, title_lbl, message_lbl, tip_lbl, record_frm):
    '''결정 버튼이 눌렸을 경우 로직'''
    if obj.addbool is False:
        mean = obj.mean_ent.get()
        # 뜻 미입력 시
        if not mean:
            show_temporarymessage(message_lbl, Text_D.WARNING_M[obj.language])
            return
        
        # 현재 단어를 word변수에 격납
        word = obj.today_word[obj.pointer]
        
        # 현재단어가 새로운 단어일 때
        if word not in obj.today_confirm and word not in obj.already_know:
            # 오늘의 단어 확정리스트와 뜻리스트에 단어 추가
            obj.today_confirm.append(obj.today_word[obj.pointer])
            obj.today_mean.append([obj.pointer + 1, mean])

            # 오른쪽 리스트에서 현재단어 초록색으로 변화
            obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_GREEN)

            # 오늘의 단어가 dayword만큼 채워졌으면 word_confirm_window
            if len(obj.today_confirm) == obj.dayword:
                obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
                obj.word_confirm_window()
                return

            # 오늘의 단어의 조회위치를 가르키는 포인터 += 1
            obj.pointer += 1

            # 다음 단어가 없을경우 db에서 dayword - len(today_confirm) + 1만큼 더 가져옴(1은 여유분)
            if obj.pointer >= len(obj.today_word):
                response = api_client.take_more_word(obj)

                if response.status_code == 200:
                    today_word_temp = response.json().get('add_word')
                    if obj.today_word == today_word_temp:
                        obj.word_confirm_window()
                        return
                    else:
                        obj.today_word = today_word_temp
                else:
                    obj.show_overframe('Instance Connection Failure')
                    return

            # 결정된 단어를 오른쪽 리스트에 추가 및 표시
            insert_word_lbl_list(obj, record_frm)
            # 현재 단어에 스크롤위젯 포커싱
            selected_scroll_widget(obj)

            # 제목, 진행률, 영단어, 뜻 입력창 갱신
            title_lbl.config(text=f'{Text_D.TITLE1[obj.language]} {obj.dayword}{Text_D.TITLE2[obj.language]}')
            obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
            obj.word_lbl.config(text=obj.today_word[obj.pointer][1])
            obj.mean_ent.delete(0, 'end')

        # 현재 단어가 이미 오늘의 단어 확정리스트에 들어가 있는 단어일때
        elif word in obj.today_confirm:
            # 뜻리스트 갱신
            for i, item in enumerate(obj.today_mean):
                if item[0] == obj.pointer + 1:
                    obj.today_mean[i] = [item[0], mean]
                    break

            # 아래는 나중에 문제없을 시 삭제할 것
            # # 오늘의 단어가 dayword만큼 채워졌으면 word_confirm_window(수정시에만 해당)
            # if len(obj.today_confirm) == obj.dayword:
            #     obj.word_confirm_window()
            #     return
        
            # 오늘의 단어의 조회위치를 가르키는 포인터 += 1
            obj.pointer += 1

            # 현재 단어에 스크롤위젯 포커싱
            selected_scroll_widget(obj)

            # 진행률, 영단어, 뜻 입력창 갱신
            obj.word_lbl.config(text=obj.today_word[obj.pointer][1])
            for item in obj.today_mean:
                if item[0] == obj.pointer + 1:
                    obj.mean_ent.delete(0, 'end')
                    obj.mean_ent.insert(0, item[1])
                    break
            else:
                obj.mean_ent.delete(0, 'end')

        # 현재 단어가 이미 아는 단어 리스트에 들어가 있는 단어일때
        else:
            # 아래는 나중에 별 문제 없으면 삭제 할 것
            # # 최종확인 윈도우에서 수정누르고 이미 아는단어를 today_confirm에 추가해버리면 
            # # len(obj.today_confirm) > obj.dayword 가 되버리는 상황 방지
            # if len(obj.today_confirm) == obj.dayword:
            #     show_temporarymessage(
            #         message_lbl,
            #         f'{Text_D.WARNING_O1[obj.language]} {obj.dayword}{Text_D.WARNING_O2[obj.language]}'
            #     )
            #     return

            # 확정리스트와 뜻리스트에 단어 추가 & 이미 아는 단어 리스트에서 삭제
            obj.today_confirm.append(obj.today_word[obj.pointer])
            obj.today_mean.append([obj.pointer + 1, mean])
            obj.already_know = [i for i in obj.already_know if i[0] != obj.pointer + 1]

            # 오른쪽 리스트에서 현재단어 초록색으로 변화
            obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_GREEN)

            # 오늘의 단어가 dayword만큼 채워졌으면 word_confirm_window
            if len(obj.today_confirm) == obj.dayword:
                obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
                obj.word_lbl_list[-1].destroy()
                obj.word_confirm_window()
                return
            
            # 오늘의 단어의 조회위치를 가르키는 포인터 += 1
            obj.pointer += 1

            # 현재 단어에 스크롤위젯 포커싱
            selected_scroll_widget(obj)

            # 진행률, 영단어, 뜻 입력창 갱신
            obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
            obj.word_lbl.config(text=obj.today_word[obj.pointer][1])
            for item in obj.today_mean:
                if item[0] == obj.pointer + 1:
                    obj.mean_ent.delete(0, 'end')
                    obj.mean_ent.insert(0, item[1])
                    break
            else:
                obj.mean_ent.delete(0, 'end')
    
    # add youself 일때
    else:
        # 영단어 or 뜻 미입력 시
        word = obj.word_ent.get()
        if not word:
            show_temporarymessage(message_lbl, Text_D.WARNING_W[obj.language])
            return
        mean = obj.mean_ent.get()
        if not mean:
            show_temporarymessage(message_lbl, Text_D.WARNING_M[obj.language])
            return
    
        # TODO: 영단어 중복검사
        # 오늘의 단어 확정리스트와 뜻리스트에 단어 추가
        if obj.pointer >= len(obj.today_confirm):
            obj.today_confirm.append([obj.pointer + 1, word])
            obj.today_mean.append([obj.pointer + 1, mean])
        
        else:
            for i, item in enumerate(obj.today_confirm):
                if item[0] == obj.pointer + 1:
                    obj.today_confirm[i] = [item[0], word]
                    break
            for i, item in enumerate(obj.today_mean):
                if item[0] == obj.pointer + 1:
                    obj.today_mean[i] = [item[0], mean]
                    break

        # 오른쪽 리스트에서 현재 단어 초록색으로 변경
        obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_GREEN)
    
        # 다음단어를 현재단어로 선정
        obj.pointer += 1

        if obj.pointer >= len(obj.word_lbl_list):
            # 오른쪽 리스트 추가 및 표시
            insert_word_lbl_list_addbool(obj, record_frm)
        selected_scroll_widget(obj)
    
        # 오늘의 단어가 dayword만큼 채워졌으면 word_confirm_window
        if len(obj.today_confirm) == obj.dayword:
            obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
            obj.word_lbl_list[-1].destroy()
            obj.word_ent.delete(0, 'end')
            obj.mean_ent.delete(0, 'end')
            obj.word_confirm_window()
            return

        # 제목, 진행률, 영단어 입력창, 뜻 입력창, 팁 갱신
        title_lbl.config(text=f'{Text_D.TITLE1[obj.language]} {obj.dayword}{Text_D.TITLE2[obj.language]}')
        obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
        if obj.pointer >= len(obj.today_confirm):
            obj.word_ent.delete(0, 'end')
            obj.mean_ent.delete(0, 'end')
        else:
            obj.word_ent.delete(0, 'end')
            obj.word_ent.insert(0, obj.today_confirm[obj.pointer][1])
            obj.mean_ent.delete(0, 'end')
            obj.mean_ent.insert(0, obj.today_mean[obj.pointer][1])
        obj.word_ent.focus()

    # 팁 갱신
    show_random_tip(obj, tip_lbl)

def already_know_word(obj, tip_lbl, record_frm):
    word = obj.today_word[obj.pointer]

    # 현재단어가 새로운 단어일 때
    if word not in obj.today_confirm and word not in obj.already_know:
        # 이미 아는 단어 리스트에 추가
        obj.already_know.append(word)

        # 오른쪽 리스트에서 현재단어 파란색으로 변화
        obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_BLUE)

        # 다음 단어를 현재단어로 변경
        obj.pointer += 1

        # 다음 단어가 없을경우 db에서 dayword - len(today_confirm) + 1만큼 더 가져옴
        if obj.pointer >= len(obj.today_word):
            response = api_client.take_more_word(obj)

            if response.status_code == 200:
                today_word_temp = response.json().get('add_word')
                if obj.today_word == today_word_temp:
                    obj.word_confirm_window()
                    return
                else:
                    obj.today_word = today_word_temp
            else:
                obj.show_overframe('Instance Connection Failure')
                return

        # 결정된 단어를 오른쪽 리스트에 추가 및 표시
        insert_word_lbl_list(obj, record_frm)
        # 현재 단어에 스크롤위젯 포커싱
        selected_scroll_widget(obj)

        # 영단어, 뜻 입력창, 팁 갱신
        obj.word_lbl.config(text=obj.today_word[obj.pointer][1])
        obj.mean_ent.delete(0, 'end')

    # 현재 단어가 이미 오늘의 단어 확정리스트에 들어가 있는 단어일때
    elif word in obj.today_confirm:
        # 오늘의 단어 확정리스트에서 제거 & 이미 아는 단어 리스트에 추가
        obj.today_confirm = [i for i in obj.today_confirm if i[0] != obj.pointer + 1]
        obj.today_mean = [i for i in obj.today_mean if i[0] != obj.pointer + 1]
        obj.already_know.append(word)

        # 오른쪽 리스트에서 현재단어 파란색으로 변화
        obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_BLUE)

        # 다음 단어를 현재단어로 변경
        obj.pointer += 1
        # 현재 단어에 스크롤위젯 포커싱
        selected_scroll_widget(obj)

        # 진행률-1, 영단어, 뜻 입력창, 팁 갱신
        obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
        obj.word_lbl.config(text=obj.today_word[obj.pointer][1])
        for item in obj.today_mean:
            if item[0] == obj.pointer + 1:
                obj.mean_ent.delete(0, 'end')
                obj.mean_ent.insert(0, item[1])
                break
        else:
            obj.mean_ent.delete(0, 'end')
    
    # 현재 단어가 이미 아는 단어 리스트에 들어가 있는 단어일때
    else:
        # 다음 단어를 현재단어로 변경
        obj.pointer += 1
        # 현재 단어에 스크롤위젯 포커싱
        selected_scroll_widget(obj)

        # 영단어, 뜻 입력창, 팁 갱신
        obj.word_lbl.config(text=obj.today_word[obj.pointer][1])
        for item in obj.today_mean:
            if item[0] == obj.pointer + 1:
                obj.mean_ent.delete(0, 'end')
                obj.mean_ent.insert(0, item[1])
                break
        else:
            obj.mean_ent.delete(0, 'end')

    # 팁 갱신
    show_random_tip(obj, tip_lbl)

def word_lbl_click(obj, n):
    '''오른쪽 프레임에서 단어를 눌렀을 경우 그 단어편집상태로 이동하는 함수'''
    # 클릭한 단어가 현재단어가 아닐경우
    if obj.pointer != n:
        # 클릭한 단어를 현재단어로 변경
        obj.pointer = n

        # 영단어, 뜻 입력창 갱신 및 스크롤바에서 선택한 단어 포커싱
        if obj.addbool:
            for item in obj.today_confirm:
                if item[0] == obj.pointer + 1:
                    obj.word_ent.delete(0, 'end')
                    obj.word_ent.insert(0, item[1])
                    break
            else:
                obj.word_ent.delete(0, 'end')

        for item in obj.today_mean:
            if item[0] == obj.pointer + 1:
                obj.mean_ent.delete(0, 'end')
                obj.mean_ent.insert(0, item[1])
                break
        else:
            obj.mean_ent.delete(0, 'end')
        selected_scroll_widget(obj)

def checkcheck(obj):
    print(f'pointer : {obj.pointer}, 스크롤바 리스트 개수 : {len(obj.word_lbl_list)}')
    print('========== today_confirm ==========')
    print(obj.today_confirm)
    print('========== today_mean ==========')
    print(obj.today_mean)