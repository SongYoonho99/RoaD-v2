'''핵심 함수 및 유틸 함수 모음 모듈'''
import re
import math
import socket
import random
import tkinter as tk
import urllib.request
from io import BytesIO
from tkinter import font
from threading import Thread
from datetime import datetime, timedelta

from gtts import gTTS
from pygame import mixer
from google import genai
from google.genai import types

from constants import Color, Font_E, Text_D, Text_T, Text_R, Tip, Gemini_instruction

# ==============================
# 유틸 함수
# ==============================
def is_internet_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except:
        pass
    try:
        urllib.request.urlopen("https://www.google.com", timeout=2)
        return True
    except:
        pass
    
    return False

def connect_audio():
    try:
        mixer.init()
        return True
    except:
        return False

def close_audio(obj):
    if obj.audio:
        mixer.quit()
    obj.root.destroy()

def place_window_center(window, width, height):
    x = window.winfo_screenwidth() // 2 - width // 2
    y = window.winfo_screenheight() // 2 - height // 2
    window.geometry(f'{width}x{height}+{x}+{y-30}')

def clear_placeholder(event):
    if event.widget.get() == 'Username':
        event.widget.delete(0, len(event.widget.get()))

def show_temp_message(message, text, color=Color.FONT_RED):
    '''입력받은 라벨에 4초간 메시지를 띄우는 함수'''
    message.config(fg=color, text=text)
    message.after(4000, lambda: message.config(text = ''))

def limit_entry_length(entry, max_len=15):
    def on_validate(new_value):
        return len(new_value) <= max_len
    vcmd = (entry.register(on_validate), '%P')
    entry.config(validate='key', validatecommand=vcmd)

def next_manual_page(
        obj, message_lbl, square_progress_lbl, square_mean_lbl, square_dict_lbl,
        square_know_lbl, square_right_lbl, next_btn, manual_window
):
    if obj.page == 0:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_{obj.page + 2}')[obj.language])
        square_progress_lbl.place(x=252, y=67)
    elif obj.page == 1:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_{obj.page + 2}')[obj.language])
        square_progress_lbl.place_forget()
        square_mean_lbl.place(x=50, y=395)
        if obj.language == 'K':
            square_dict_lbl.place(x=199, y=573)
        else:
            square_dict_lbl.place(x=83, y=572)
    elif obj.page == 2:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_{obj.page + 2}')[obj.language])
        square_mean_lbl.place_forget()
        square_dict_lbl.place_forget()
        square_know_lbl.place(x=58, y=366)
    elif obj.page == 3:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_{obj.page + 2}')[obj.language])
        square_know_lbl.place_forget()
        square_right_lbl.place(x=645)
        next_btn.config(text=Text_D.START[obj.language])
    else:
        manual_window.destroy()
        return

    obj.page += 1

def next_manual_page_add(
        obj, message_lbl, square_progress_lbl, square_word_lbl, square_mean_lbl,
        square_right_add_lbl, next_btn, manual_window
):
    if obj.page == 0:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_{obj.page + 2}')[obj.language])
        square_progress_lbl.place(x=252, y=67)
    elif obj.page == 1:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_ADD_{obj.page + 2}')[obj.language])
        square_progress_lbl.place_forget()
        square_word_lbl.place(x=119, y=205)
        square_mean_lbl.place(x=52, y=369)
    elif obj.page == 2:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_ADD_{obj.page + 2}')[obj.language])
        square_word_lbl.place_forget()
        square_mean_lbl.place_forget()
        square_right_add_lbl.place(x=643)
        next_btn.config(text=Text_D.START[obj.language])
    else:
        manual_window.destroy()
        return

    obj.page += 1

def typing_effect(label, text, delay=75, callback=None):
    '''Label의 글자를 한 글자씩 출력'''
    fnt = font.Font(font=label['font'])
    label.config(width=max(1, fnt.measure(text) // fnt.measure('e'))) # e 가 한글, 일본어 양쪽대응

    def inner(idx=0):
        if idx <= len(text):
            label.config(text=text[:idx])
            label.after(delay, inner, idx+1)
        elif callback:
            callback()
    inner()

def copy_word(obj, event):
    obj.clipboard_clear()
    obj.clipboard_append(obj.word_lbl.cget('text'))
    event.widget.config(image=obj.controller.check_icon)
    event.widget.after(2000, lambda: event.widget.config(image=obj.controller.copy_icon))

def copy_url(obj, event):
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
    if obj.controller.audio:
        tts = gTTS(text=word, lang='en')
        mp3_crt = BytesIO()
        tts.write_to_fp(mp3_crt)
        mp3_crt.seek(0)
        mixer.music.load(mp3_crt, 'mp3')
        mixer.music.play()

def on_mousewheel(event, canvas):
    canvas.yview_scroll(-1 * (event.delta // 120), 'units')

def on_configure(event, canvas):
    bbox = canvas.bbox('all')
    if bbox:
        canvas.configure(
            scrollregion=(0, 0, canvas.winfo_width(), max(bbox[3], canvas.winfo_height()))
        )

def _resize_record_frame(obj, event):
    canvas_width = event.width
    obj.canvas.itemconfig(obj.window_id, width=canvas_width)
    obj.record_frm.config(width=canvas_width)

def show_daily_tip(obj, tip_lbl):
    '''TIP_D 또는 TIP_B로 시작하는 항목 중 하나를 랜덤 출력'''
    tip_attrs = [
        v for k, v in Tip.__dict__.items()
        if (k.startswith('TIP_D') or k.startswith('TIP_B')) and isinstance(v, dict)
    ]
    tip = random.choice(tip_attrs)
    tip_lbl.config(text=tip[obj.language])

def show_test_tip(obj, tip_lbl):
    '''TIP_D 또는 TIP_B로 시작하는 항목 중 하나를 랜덤 출력'''
    tip_attrs = [
        v for k, v in Tip.__dict__.items()
        if (k.startswith('TIP_T') or k.startswith('TIP_B')) and isinstance(v, dict)
    ]
    tip = random.choice(tip_attrs)
    tip_lbl.config(text=tip[obj.language])

def insert_lbl_list(obj, record_frm):
    '''DailyFrame 오른쪽 리스트에 단어 추가하는 함수'''
    lbl = tk.Label(
        record_frm, bg=Color.DEEP, font=Font_E.BODY, anchor='w',
        highlightthickness=5, highlightbackground=Color.DEEP, 
        text=f'{obj.pointer + 1}. {obj.today_word[obj.pointer]}'
    )
    lbl.pack(padx=(4, 0), fill='x')
    lbl.bind('<MouseWheel>', lambda e: on_mousewheel(e, obj.canvas))
    lbl.bind('<Button-1>', lambda e, i=len(obj.word_lbl_list): click_word_lbl(obj, i))
    obj.word_lbl_list.append(lbl)
    record_frm.update_idletasks()
    record_frm.master.yview_moveto(1.0)

def insert_lbl_list_add_yourself(obj, record_frm):
    '''DailyFrame 오른쪽 리스트에 단어 추가하는 함수(add yourself일때)'''
    lbl = tk.Label(
        record_frm, bg=Color.DEEP, font=Font_E.BODY, anchor='w',
        highlightthickness=5, highlightbackground = Color.DEEP, 
        text=f'{obj.pointer + 1}. '
    )
    lbl.pack(padx=(4, 0), fill='x')
    lbl.bind('<MouseWheel>', lambda e: on_mousewheel(e, obj.canvas))
    lbl.bind('<Button-1>', lambda e, i=len(obj.word_lbl_list): click_word_lbl(obj, i))
    obj.word_lbl_list.append(lbl)
    record_frm.update_idletasks()
    record_frm.master.yview_moveto(1.0)

    # Entry 입력 감지
    text_var = tk.StringVar()
    obj.word_ent.config(textvariable=text_var)
    text_var.trace_add('write',
        lambda *_: obj.word_lbl_list[obj.pointer].config(text=f'{obj.pointer + 1}. {text_var.get()}')
    )

def renew_wordlbl_meanent(obj):
    obj.word_lbl.config(text=obj.today_word[obj.pointer])
    obj.mean_ent.delete(0, 'end')
    for w, m in obj.today_confirm:
        if w == obj.today_word[obj.pointer]:
            obj.mean_ent.insert(0, m)
            break
        
def renew_ent_add_yourself(obj):
    obj.word_ent.delete(0, 'end')
    if obj.pointer < len(obj.today_confirm):
        obj.word_ent.insert(0, obj.today_confirm[obj.pointer][0])
    obj.mean_ent.delete(0, 'end')
    if obj.pointer < len(obj.today_confirm):
        obj.mean_ent.insert(0, obj.today_confirm[obj.pointer][1])

def selected_scroll_widget(obj):
    '''pointer가 가르키는 스크롤바 내 라벨색상을 DAKR, 그 외에는 DEEP'''
    for i, lbl in enumerate(obj.word_lbl_list):
        if i == obj.pointer:
            lbl.config(bg=Color.DARK, highlightbackground=Color.DARK)
        else:
            lbl.config(bg=Color.DEEP, highlightbackground=Color.DEEP)

def change_mean(obj, n):
    if obj.btn_list[n]['bg'] == Color.BEIGE:
        obj.btn_list[n].config(bg=Color.GREEN)
        obj.lbl_list[n].grid_forget()
        obj.ent_list[n].grid(row=n, column=2, sticky='ew')
        obj.ent_list[n].focus_set()
    else:
        obj.today_confirm[n][1] = obj.ent_list[n].get()
        obj.btn_list[n].config(bg=Color.BEIGE)
        obj.ent_list[n].grid_forget()
        obj.lbl_list[n].config(text=obj.today_confirm[n][1])
        obj.lbl_list[n].grid(row=n, column=2, sticky='ew')

def insert_lbl_list_test(obj):
    '''DailyFrame 오른쪽 리스트에 단어 추가하는 함수'''
    lbl = tk.Label(
        obj.record_frm, bg=Color.DEEP, font=Font_E.BODY, anchor='w',
        highlightthickness=5, highlightbackground=Color.DEEP, 
        text=f'{obj.pointer + 1}. {obj.word_list[obj.pointer]}'
    )
    lbl.pack(padx=(4, 0), fill='x')
    lbl.bind('<MouseWheel>', lambda e: on_mousewheel(e, obj.canvas))
    lbl.bind(
        '<Button-1>',
        lambda e, i=len(obj.word_lbl_list):
            click_word_lbl_test(obj, i) if not obj.is_scoring else None
    )
    obj.word_lbl_list.append(lbl)
    obj.record_frm.update_idletasks()
    obj.record_frm.master.yview_moveto(1.0)

def animate_score(obj, label, score):
    current = 0

    def update():
        nonlocal current
        if current >= score:
            label.config(text=f'{score}{Text_R.SCORE[obj.language]}')
            obj.review_lbl.config(fg=Color.FONT_DEFAULT)
            obj.review_btn.config(bg=Color.GREEN, fg=Color.FONT_DEFAULT, relief='raised')
            return

        current += 1
        label.config(text=f'{current}{Text_R.SCORE[obj.language]}')

        min_delay = 20
        max_delay = 500
        exponent = 10
        ratio = current / score
        delay = int(min_delay + (max_delay - min_delay) * (ratio ** exponent))

        label.after(delay, update)

    update()

# ==============================
# 프로그램 로직 함수
# ==============================
def select_streak_message(streak, language):
    if streak is False:
        return Text_D.INITIAL_LOGIN[language]
    elif streak is True:
        return Text_D.DONE_TODAY[language]
    elif streak > 0:
        return f'{streak} {Text_D.STREAK_P[language]}'
    else:
        return f'{-streak} {Text_D.STREAK_N[language]}'

def _on_decision_click_new(obj, word, mean, message_lbl, record_frm):
    # today_confirm 에 단어 추가
    obj.today_confirm.append([word, mean])
    obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_GREEN)

    # 오늘의 단어 dayword개 채우기 성공
    if len(obj.today_confirm) == obj.dayword:
        obj.open_confirm_word_window()
        return

    obj.pointer += 1

    # 다음 단어가 없을경우 db에서 딱 필요한 만큼 더 가져옴
    if obj.pointer == len(obj.today_word):
        from connector import take_more_word
        added_word = take_more_word(obj, message_lbl)
        if added_word is False:
            return
        # db에 더이상 가져올 단어가 없어서 가져왔는데도 불구하고 이전이랑 똑같을 경우 성공
        if not added_word:
            obj.open_confirm_word_window()
            return
        obj.today_word += added_word

    insert_lbl_list(obj, record_frm)

def _on_decision_click_confirm(obj, word, mean):
    # today_mean 갱신
    for i, (w, _) in enumerate(obj.today_confirm):
        if w == word:
            obj.today_confirm[i][1] = mean
            break

    obj.pointer += 1

def _on_decision_click_already(obj, word, mean):
    # today_confirm 에 단어 추가 & already_know 에서 단어 삭제
    obj.today_confirm.append([word, mean])
    obj.already_know = [w for w in obj.already_know if w != word]
    obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_GREEN)

    # 오늘의 단어 dayword개 채우기 성공
    if len(obj.today_confirm) == obj.dayword:
        obj.word_lbl_list[-1].destroy()
        obj.word_lbl_list.pop()
        obj.open_confirm_word_window()
        return
    
    obj.pointer += 1

def _on_decision_click_add(obj, word, mean, record_frm):
    # 새로운 단어일 경우 리스트에 단어와 뜻을 추가
    if obj.pointer == len(obj.today_confirm):
        obj.today_confirm.append([word, mean])
        obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_GREEN)

        # 오늘의 단어 dayword개 채우기 성공
        if len(obj.today_confirm) == obj.dayword:
            obj.open_confirm_word_window()
            return
    
    # 새로운 단어가 아닐 경우 갱신
    else:
        obj.today_confirm[obj.pointer] = [word, mean]
    
    obj.pointer += 1
    if obj.pointer == len(obj.word_lbl_list):
        insert_lbl_list_add_yourself(obj, record_frm)

def on_decision_click(obj, title_lbl, message_lbl, tip_lbl, record_frm):
    if obj.is_add_yourself is False:
        word = obj.today_word[obj.pointer]
        mean = obj.mean_ent.get()

        if not mean:
            show_temp_message(message_lbl, Text_D.WARNING_M[obj.language])
            return
        
        if all(word != w[0] for w in obj.today_confirm) and word not in obj.already_know:
            _on_decision_click_new(obj, word, mean, message_lbl, record_frm)
        elif any(word == w[0] for w in obj.today_confirm):
            _on_decision_click_confirm(obj, word, mean)
        else:
            _on_decision_click_already(obj, word, mean)
        
        renew_wordlbl_meanent(obj)
    
    else:
        word = obj.word_ent.get()
        mean = obj.mean_ent.get()

        if not word:
            show_temp_message(message_lbl, Text_D.WARNING_W[obj.language])
            return
        if not re.fullmatch(r"[A-Za-z ']*", word):
            show_temp_message(message_lbl, Text_D.WARNING_W[obj.language])
            return
        if not mean:
            show_temp_message(message_lbl, Text_D.WARNING_M[obj.language])
            return
        if any(word == w[0] for i, w in enumerate(obj.today_confirm) if i != obj.pointer):
            show_temp_message(message_lbl, Text_D.WARNING_D[obj.language])
            return
        
        _on_decision_click_add(obj, word, mean, record_frm)
        renew_ent_add_yourself(obj)
        obj.word_ent.focus()

    selected_scroll_widget(obj)
    title_lbl.config(text=f'{Text_D.TITLE1[obj.language]} {obj.dayword}{Text_D.TITLE2[obj.language]}')
    obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
    show_daily_tip(obj, tip_lbl)

def _on_already_click_new(obj, word, message_lbl, record_frm):
    # already_know 에 단어 추가
    obj.already_know.append(word)
    obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_BLUE)

    obj.pointer += 1

    # 다음 단어가 없을경우 db에서 딱 필요한 만큼 더 가져옴
    if obj.pointer >= len(obj.today_word):
        from connector import take_more_word
        added_word = take_more_word(obj, message_lbl)
        if added_word is False:
            return
        # db에 더이상 가져올 단어가 없어서 가져왔는데도 불구하고 이전이랑 똑같을 경우 성공
        if not added_word:
            obj.open_confirm_word_window()
            return
        obj.today_word = obj.today_word + added_word

    insert_lbl_list(obj, record_frm)

def _on_already_click_confirm(obj, word):
    # today_confirm 에서 단어 제거 & already_know 에 단어 추가
    obj.today_confirm = [i for i in obj.today_confirm if i[0] != word]
    obj.already_know.append(word)
    obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_BLUE)

    obj.pointer += 1

def _on_already_click_already(obj):
    obj.pointer += 1

def on_already_click(obj, tip_lbl, message_lbl, record_frm):
    word = obj.today_word[obj.pointer]

    if all(word != w[0] for w in obj.today_confirm) and word not in obj.already_know:
        _on_already_click_new(obj, word, message_lbl, record_frm)
    elif any(word == w[0] for w in obj.today_confirm):
        _on_already_click_confirm(obj, word)
    else:
        _on_already_click_already(obj)

    selected_scroll_widget(obj)
    obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
    renew_wordlbl_meanent(obj) 
    show_daily_tip(obj, tip_lbl)

def click_word_lbl(obj, n):
    if obj.pointer == n:
        return
    
    prev = obj.pointer
    obj.pointer = n   

    if obj.is_add_yourself is False:
        renew_wordlbl_meanent(obj)
    else:
        # add yourself에서 StringVar 때문에 저장하지 않은 글자가 오른쪽리스트에 반영되는 문제 해결
        if prev == len(obj.today_confirm):
            obj.word_lbl_list[prev].config(text=f'{prev + 1}. ')
        else:
            obj.word_lbl_list[prev].config(text=f'{prev + 1}. {obj.today_confirm[prev][0]}')

        renew_ent_add_yourself(obj)

    selected_scroll_widget(obj)

def start_test(
        obj, username, language, is_add_yourself, streak,
        lbl = None, window = None, is_exist_today_word = True
    ):
    from connector import write_today_word, get_test_data
    
    if is_exist_today_word:
        if not all(btn['bg'] == Color.BEIGE for btn in obj.btn_list):
            show_temp_message(lbl, Text_D.WARNING_C[language])
            return

        window.destroy()

        if not write_today_word(obj):
            return
        
    response = get_test_data(obj, username)
    if response is False:
        return
    
    test_word = (
        [5] + response.get('fifth')
        + [4] + response.get('fourth')
        + [3] + response.get('third')
        + [2] + response.get('second')
        + [1] + response.get('first')
    )
    if is_exist_today_word:
        test_word += ['today'] + obj.today_confirm

    test_frm = obj.controller.frames['TestFrame']
    test_frm.init_data(username, language, is_add_yourself, streak, test_word)
    test_frm.create_widgets()
    show_next_word(test_frm)
    obj.controller.show_frame('TestFrame')

def click_submit_btn(obj):
    word = obj.word_lbl.cget('text')
    user_answer = obj.mean_ent.get()   

    # input_frm 에서 review_frm 으로 변경
    obj.input_frm.pack_forget()
    obj.tip_lbl.pack_forget()
    obj.review_frm.pack(padx=25, pady=(0, 17))
    obj.tip_lbl.pack(side='left', padx=20, pady=(0, 20))

    # input_frm, review_frm 갱신
    obj.mean_ent.delete(0, 'end')
    obj.result_lbl.config(fg=Color.FONT_DARK, text='O')
    obj.user_answer_lbl.config(text=user_answer, fg=Color.FONT_DEFAULT)
    obj.model_answer_lbl.config(text=obj.model_answer_list[obj.pointer]) 
    obj.comment_lbl.config(text='')
    obj.next_btn.config(state='disabled', bg=Color.BEIGE)
    obj.is_scoring = True
    obj.update_idletasks()

    Thread(target=_run_grading_thread, args=(obj, word, user_answer), daemon=True).start()

def _run_grading_thread(obj, word, user_answer):
    result, comment = _give_marks(word, user_answer, obj.language)
    obj.after(0, lambda: _update_ui_after_grading(obj, user_answer, result, comment))

def _give_marks(word, user_answer, language):
    # if 'client' not in globals():
    #     global client
    #     client = genai.Client(api_key=os.getenv('GEMINI_API'))

    # contents = f'''
    #     "english_word": {word},
    #     "student's_answer": {user_answer}
    # '''

    # try:
    #     response = client.models.generate_content(
    #         model="gemini-2.5-flash",
    #         config=types.GenerateContentConfig(
    #             system_instruction=Gemini_instruction[language]),
    #         contents=contents
    #     )
    #     result = response.text[0]
    #     comment = response.text[1:].strip()
    #     if result not in ['O', 'X', 'o', 'x']:
    #         result = '-'
    #         comment = Text_T.GEMINI_ERROR[language]

    # except:
    #     try:
    #         response = client.models.generate_content(
    #             model="gemini-2.5-flash-lite",
    #             config=types.GenerateContentConfig(
    #                 system_instruction=Gemini_instruction[language]),
    #             contents=contents
    #         )
    #         result = response.text[0]
    #         comment = response.text[1:].strip()
    #         if result not in ['O', 'X', 'o', 'x']:
    #             result = '-'
    #             comment = Text_T.GEMINI_ERROR[language]

    #     except:
    #         result = '-'
    #         comment = Text_T.GEMINI_ERROR[language]

    # return result, comment

    return 'x', 'yes'

def _update_ui_after_grading(obj, user_answer, result, comment):
    # 결과에 따른 색 지정
    if result in ['O', 'o']:
        obj.result_lbl.config(fg=Color.FONT_GREEN)
        obj.user_answer_lbl.config(fg=Color.FONT_GREEN)
        obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_GREEN)
    elif result in ['X', 'x']:
        obj.result_lbl.config(fg=Color.FONT_RED)
        obj.user_answer_lbl.config(fg=Color.FONT_RED)
        obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_RED)
    else:
        obj.result_lbl.config(fg=Color.FONT_DEFAULT)

    # 결과, 유저의 입력, 코멘트 리스트에 격납
    obj.result_list.append(result)
    obj.user_answer_list.append(user_answer)
    obj.comment_list.append(comment)

    # 채점 결과, 코멘트 표시, 버튼, 오른쪽 라벨 다시 활성화
    obj.result_lbl.config(text=result)
    obj.comment_lbl.config(text=comment)
    obj.next_btn.config(state='normal', bg=Color.GREEN)
    obj.is_scoring = False
    if len(obj.result_list) == obj.number_of_word:
        obj.next_btn.config(text=Text_T.SHOW_RESULT[obj.language])

    obj.pointer += 1

def show_next_word(obj, is_return_current = False):
    if is_return_current and len(obj.word_list) == len(obj.user_answer_list):
        obj.is_return_current = False
        obj.pointer = len(obj.word_list)
        show_next_word(obj)
        return
    elif is_return_current:
        _return_current(obj)
        return

    while obj.now_pointer < len(obj.test_word):
        current = obj.test_word[obj.now_pointer]

        if isinstance(current, int):
            obj.number_of_iteration = current
            obj.now_pointer += 1
            continue

        if isinstance(current, str):
            obj.date_temp = _decide_date(obj, current)
            obj.now_pointer += 1
            continue
            
        if isinstance(current, list):         
            # review_frm 에서 input_frm 으로 변경
            obj.review_frm.pack_forget()
            obj.tip_lbl.pack_forget()
            obj.input_frm.pack(padx=55, pady=(80, 120))
            obj.tip_lbl.pack(side='left', padx=20, pady=(0, 20))

            # 단어 등록 날짜, 단어, 모범답안 리스트에 격납
            obj.date_lbl_list.append(obj.date_temp)
            obj.word_list.append(current[0])
            obj.model_answer_list.append(current[1])

            # input_frm 표시
            obj.date_lbl.config(text=obj.date_temp)
            obj.progress_lbl.config(text=f'{len(obj.word_list)} / {obj.number_of_word}')
            obj.word_lbl.config(text=current[0])
            obj.mean_ent.focus_set()
            insert_lbl_list_test(obj)
            selected_scroll_widget(obj)
            show_test_tip(obj, obj.tip_lbl)

            # test_word의 마지막인덱스를 가르키는 포인터 1 증가
            obj.now_pointer += 1

            return

    finish_test(obj)

def _decide_date(obj, current):
    if current == 'today':
        date_confirm = Text_T.DATE_TODAY[obj.language]
    else:
        if obj.number_of_iteration == 5:
            date_confirm = (datetime.strptime(current, '%Y-%m-%d') - timedelta(days=28)).strftime('%Y-%m-%d')
        elif obj.number_of_iteration == 4:
            date_confirm = (datetime.strptime(current, '%Y-%m-%d') - timedelta(days=14)).strftime('%Y-%m-%d')
        elif obj.number_of_iteration == 3:
            date_confirm = (datetime.strptime(current, '%Y-%m-%d') - timedelta(days=7)).strftime('%Y-%m-%d')
        elif obj.number_of_iteration == 2:
            date_confirm = (datetime.strptime(current, '%Y-%m-%d') - timedelta(days=3)).strftime('%Y-%m-%d')
        elif obj.number_of_iteration == 1:
            date_confirm = (datetime.strptime(current, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
        
        date_confirm = date_confirm[5:].replace('-', '/') + Text_T.DATE_TEXT1[obj.language]

        if obj.number_of_iteration == 5:
            date_confirm += Text_T.DATE_TEXT3[obj.language]
        else:
            date_confirm += f'{obj.number_of_iteration}' + Text_T.DATE_TEXT2[obj.language]
    
    return date_confirm

def click_word_lbl_test(obj, n):
    # 현재 단어와 같은 단어를 클릭했을 시
    if obj.pointer == n:
        return
    
    obj.pointer = n

    # 가장 최근 출력된 단어를 클릭했을 시
    if obj.pointer == len(obj.word_list) - 1:
        # 가장 최근 출력된 단어가 리뷰상태인 경우
        if len(obj.word_list) == len(obj.user_answer_list) + 1:
            _return_current(obj)
            return
    
    obj.is_return_current = True
    
    # input_frm 에서 review_frm 으로 변경
    obj.input_frm.pack_forget()
    obj.tip_lbl.pack_forget()
    obj.review_frm.pack(padx=25, pady=(0, 17))
    obj.tip_lbl.pack(side='left', padx=20, pady=(0, 20))

    # review_frm 표시
    obj.date_lbl.config(text=obj.date_lbl_list[obj.pointer])
    obj.word_lbl.config(text=obj.word_list[obj.pointer])
    obj.result_lbl.config(text=obj.result_list[obj.pointer])
    obj.user_answer_lbl.config(text=obj.user_answer_list[obj.pointer])
    if obj.result_list[obj.pointer] in ['O', 'o']:
        obj.result_lbl.config(fg=Color.FONT_GREEN)
        obj.user_answer_lbl.config(fg=Color.FONT_GREEN)
    elif obj.result_list[obj.pointer] in ['X', 'x']:
        obj.result_lbl.config(fg=Color.FONT_RED)
        obj.user_answer_lbl.config(fg=Color.FONT_RED)
    else:
        obj.result_lbl.config(fg=Color.FONT_DEFAULT)
        obj.user_answer_lbl.config(fg=Color.FONT_DEFAULT)
    obj.model_answer_lbl.config(text=obj.model_answer_list[obj.pointer])
    obj.comment_lbl.config(text=obj.comment_list[obj.pointer])
    selected_scroll_widget(obj)

def _return_current(obj):
    obj.pointer = len(obj.word_list) - 1
    obj.is_return_current = False

    # review_frm 에서 input_frm 으로 변경
    obj.review_frm.pack_forget()
    obj.tip_lbl.pack_forget()
    obj.input_frm.pack(padx=55, pady=(80, 120))
    obj.tip_lbl.pack(side='left', padx=20, pady=(0, 20))

    # input_frm 표시
    obj.date_lbl.config(text=obj.date_lbl_list[obj.pointer])
    obj.word_lbl.config(text=obj.word_list[obj.pointer])
    selected_scroll_widget(obj)

def finish_test(obj):
    # TODO: DB에 기록

    obj.winfo_toplevel().unbind('<Return>')
    obj.mean_ent.unbind('<Return>')

    wrong_date_list = []
    wrong_word_list = []
    wrong_user_answer_list = []
    wrong_model_answer_list = []
    wrong_comment_list = []
    
    for i, result in enumerate(obj.result_list):
        if result in ['X', 'x']:
            wrong_date_list.append(obj.date_lbl_list[i])
            wrong_word_list.append(obj.word_list[i])
            wrong_user_answer_list.append(obj.user_answer_list[i])
            wrong_model_answer_list.append(obj.model_answer_list[i])
            wrong_comment_list.append(obj.comment_list[i])
    
    result_frm = obj.controller.frames['ResultFrame']
    result_frm.init_data(
        obj.username, obj.language, obj.number_of_word, wrong_date_list, wrong_word_list,
        wrong_user_answer_list, wrong_model_answer_list, wrong_comment_list
    )
    result_frm.create_widgets()
    obj.controller.show_frame('ResultFrame')

def show_wrong_word(obj, title_lbl):
    title_lbl.pack()
    obj.review_frm.place_forget()
    obj.check_frm.pack(expand=True)
    show_next_word_result(obj)

def show_next_word_result(obj):
    obj.date_lbl.config(text=obj.date_list[obj.pointer])
    obj.word_lbl.config(text=obj.word_list[obj.pointer])
    obj.user_answer_lbl.config(text=obj.user_answer_list[obj.pointer])
    obj.model_answer_lbl.config(text=obj.model_answer_list[obj.pointer])
    obj.comment_lbl.config(text=obj.comment_list[obj.pointer])

    obj.pointer += 1

def click_word_lbl_result(obj, n):
    if obj.pointer == n:
        return
    
    obj.pointer = n

    show_next_word_result(obj)