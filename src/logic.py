'''핵심 함수 및 유틸 함수 모음 모듈'''
import re
import socket
import random
import tkinter as tk
import urllib.request
from io import BytesIO
from tkinter import font

from gtts import gTTS
from pygame import mixer

from constants import Color, Font_E, Text_D, Tip

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
        square_progress_lbl.place(x=250, y=67)
    elif obj.page == 1:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_{obj.page + 2}')[obj.language])
        square_progress_lbl.place_forget()
        square_mean_lbl.place(x=48, y=395)
        if obj.language == 'K':
            square_dict_lbl.place(x=197, y=573)
        else:
            square_dict_lbl.place(x=81, y=572)
    elif obj.page == 2:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_{obj.page + 2}')[obj.language])
        square_mean_lbl.place_forget()
        square_dict_lbl.place_forget()
        square_know_lbl.place(x=56, y=366)
    elif obj.page == 3:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_{obj.page + 2}')[obj.language])
        square_know_lbl.place_forget()
        square_right_lbl.place(x=643)
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
        square_progress_lbl.place(x=250, y=67)
    elif obj.page == 1:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_ADD_{obj.page + 2}')[obj.language])
        square_progress_lbl.place_forget()
        square_word_lbl.place(x=117, y=205)
        square_mean_lbl.place(x=50, y=369)
    elif obj.page == 2:
        message_lbl.config(text=getattr(Text_D, f'MANUAL_ADD_{obj.page + 2}')[obj.language])
        square_word_lbl.place_forget()
        square_mean_lbl.place_forget()
        square_right_add_lbl.place(x=641)
        next_btn.config(text=Text_D.START[obj.language])
    else:
        manual_window.destroy()
        return

    obj.page += 1

def typing_effect(label, text, delay=75):
    '''Label의 글자를 한 글자씩 출력'''
    fnt = font.Font(font=label['font'])
    label.config(width=max(1, fnt.measure(text) // fnt.measure('e'))) # e 가 한글, 일본어 양쪽대응

    def inner(idx=0):
        if idx <= len(text):
            label.config(text=text[:idx])
            label.after(delay, inner, idx+1)
    inner()

def copy_word(obj, event):
    text_to_copy = obj.word_lbl.cget('text')
    obj.clipboard_clear()
    obj.clipboard_append(text_to_copy)
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
        mixer.music.load(mp3_crt, "mp3")
        mixer.music.play()

def on_mousewheel(event, canvas):
    canvas.yview_scroll(-1 * (event.delta // 120), 'units')

def on_configure(event, canvas):
    bbox = canvas.bbox('all')
    if bbox:
        canvas.configure(
            scrollregion=(0, 0, canvas.winfo_width(), max(bbox[3], canvas.winfo_height()))
        )

def show_daily_tip(obj, tip_lbl):
    '''TIP_D 또는 TIP_B로 시작하는 항목 중 하나를 랜덤 출력'''
    tip_attrs = [
        v for k, v in Tip.__dict__.items()
        if (k.startswith('TIP_D') or k.startswith('TIP_B')) and isinstance(v, dict)
    ]
    tip = random.choice(tip_attrs)
    tip_lbl.config(text=tip[obj.language])

def insert_lbl_list(obj, record_frm):
    '''DailyFrame 오른쪽 리스트에 단어 추가하는 함수'''
    lbl = tk.Label(
        record_frm, bg=Color.DEEP, font=Font_E.BODY, anchor='w',
        highlightthickness=5, highlightbackground=Color.DEEP, 
        text=f'{obj.pointer + 1}. {obj.today_word[obj.pointer][1]}'
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
        obj.today_mean[n][1] = obj.ent_list[n].get()
        obj.btn_list[n].config(bg=Color.BEIGE)
        obj.ent_list[n].grid_forget()
        obj.lbl_list[n].config(text=obj.today_mean[n][1])
        obj.lbl_list[n].grid(row=n, column=2, sticky='ew')

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

def _on_decision_click_new(obj, mean, title_lbl, message_lbl, record_frm):
    # today_confirm, today_mean 에 단어 추가
    obj.today_confirm.append(obj.today_word[obj.pointer])
    obj.today_mean.append([obj.pointer + 1, mean])
    obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_GREEN)

    # 오늘의 단어 dayword개 채우기 성공
    if len(obj.today_confirm) == obj.dayword:
        obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
        obj.open_confirm_word_window()
        return

    # 다음단어를 현재단어로 선정
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
        else:
            obj.today_word = obj.today_word + added_word

    insert_lbl_list(obj, record_frm)
    selected_scroll_widget(obj)

    # 제목, 진행률, 영단어, 뜻 입력창 갱신
    title_lbl.config(text=f'{Text_D.TITLE1[obj.language]} {obj.dayword}{Text_D.TITLE2[obj.language]}')
    obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
    obj.word_lbl.config(text=obj.today_word[obj.pointer][1])
    obj.mean_ent.delete(0, 'end')

def _on_decision_click_confirm(obj, mean):
    # today_mean 갱신
    for i, item in enumerate(obj.today_mean):
        if item[0] == obj.pointer + 1:
            obj.today_mean[i] = [item[0], mean]
            break

    # 다음단어를 현재단어로 선정
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

def _on_decision_click_already(obj, mean):
    # today_confirm, today_mean 에 단어 추가 & already_know 에서 단어 삭제
    obj.today_confirm.append(obj.today_word[obj.pointer])
    obj.today_mean.append([obj.pointer + 1, mean])
    obj.already_know = [i for i in obj.already_know if i[0] != obj.pointer + 1]
    obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_GREEN)

    # 오늘의 단어 dayword개 채우기 성공
    if len(obj.today_confirm) == obj.dayword:
        obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
        obj.word_lbl_list[-1].destroy()
        obj.word_lbl_list.pop()
        obj.open_confirm_word_window()
        return
    
    # 오늘의 단어의 조회위치를 가르키는 포인터 += 1
    obj.pointer += 1
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

def _on_decision_click_add(obj, word, mean, title_lbl, record_frm):
    # 새로운 단어일 경우 리스트에 단어와 뜻을 추가
    if obj.pointer >= len(obj.today_confirm):
        obj.today_confirm.append([obj.pointer + 1, word])
        obj.today_mean.append([obj.pointer + 1, mean])
        obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_GREEN)

        # 오늘의 단어 dayword개 채우기 성공
        if len(obj.today_confirm) == obj.dayword:
            obj.progress_lbl.config(text=f'{len(obj.today_confirm)} / {obj.dayword}')
            obj.open_confirm_word_window()
            return
    
    # 새로운 단어가 아닐 경우 갱신
    else:
        for item in obj.today_confirm:
            if item[0] == obj.pointer + 1:
                obj.today_confirm[obj.pointer] = [item[0], word]
                break
        for item in obj.today_mean:
            if item[0] == obj.pointer + 1:
                obj.today_mean[obj.pointer] = [item[0], mean]
                break
    
    # 다음단어를 현재단어로 선정
    obj.pointer += 1
    if obj.pointer >= len(obj.word_lbl_list):
        insert_lbl_list_add_yourself(obj, record_frm)
    selected_scroll_widget(obj)

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

def on_decision_click(obj, title_lbl, message_lbl, tip_lbl, record_frm):
    if obj.is_add_yourself is False:
        word = obj.today_word[obj.pointer]
        mean = obj.mean_ent.get()
        if not mean:
            show_temp_message(message_lbl, Text_D.WARNING_M[obj.language])
            return
        
        if word not in obj.today_confirm and word not in obj.already_know:
            _on_decision_click_new(obj, mean, title_lbl, message_lbl, record_frm)
        elif word in obj.today_confirm:
            _on_decision_click_confirm(obj, mean)
        else:
            _on_decision_click_already(obj, mean)
    
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
        if any(word == w[1] for i, w in enumerate(obj.today_confirm) if i != obj.pointer):
            show_temp_message(message_lbl, Text_D.WARNING_D[obj.language])
            return
        
        _on_decision_click_add(obj, word, mean, title_lbl, record_frm)

    show_daily_tip(obj, tip_lbl)

def _on_already_click_new(obj, word, message_lbl, record_frm):
    # already_know 에 단어 추가
    obj.already_know.append(word)
    obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_BLUE)

    # 다음 단어를 현재단어로 변경
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
        else:
            obj.today_word = obj.today_word + added_word

    # 결정된 단어를 오른쪽 리스트에 추가 및 표시
    insert_lbl_list(obj, record_frm)
    # 현재 단어에 스크롤위젯 포커싱
    selected_scroll_widget(obj)

    # 영단어, 뜻 입력창, 팁 갱신
    obj.word_lbl.config(text=obj.today_word[obj.pointer][1])
    obj.mean_ent.delete(0, 'end')

def _on_already_click_confirm(obj, word):
    # today_confirm 에서 단어 제거 & already_know 에 단어 추가
    obj.today_confirm = [i for i in obj.today_confirm if i[0] != obj.pointer + 1]
    obj.today_mean = [i for i in obj.today_mean if i[0] != obj.pointer + 1]
    obj.already_know.append(word)
    obj.word_lbl_list[obj.pointer].config(fg=Color.FONT_BLUE)

    # 다음 단어를 현재단어로 변경
    obj.pointer += 1
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

def _on_already_click_already(obj):
    # 다음 단어를 현재단어로 변경
    obj.pointer += 1
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

def on_already_click(obj, tip_lbl, message_lbl, record_frm):
    word = obj.today_word[obj.pointer]

    if word not in obj.today_confirm and word not in obj.already_know:
        _on_already_click_new(obj, word, message_lbl, record_frm)
    elif word in obj.today_confirm:
        _on_already_click_confirm(obj, word)
    else:
        _on_already_click_already(obj)

    show_daily_tip(obj, tip_lbl)

def click_word_lbl(obj, n):
    if obj.pointer != n:
        # add yourself에서 StringVar 때문에 저장하지 않은 글자가 오른쪽리스트에 반영되는 문제 해결
        if obj.is_add_yourself and obj.pointer < len(obj.today_confirm) - 1:
            obj.word_lbl_list[obj.pointer].config(text=f'{obj.pointer + 1}. {obj.today_confirm[obj.pointer][1]}')

        obj.pointer = n

        # add yourself == False 일 경우, word_ent 조정
        if not obj.is_add_yourself:
            for item in obj.today_word:
                if item[0] == obj.pointer + 1:
                    obj.word_lbl.config(text=obj.today_word[obj.pointer][1])
                    break
        # add yourself == True 일 경우, word_lbl 조정
        else:
            for item in obj.today_confirm:
                if item[0] == obj.pointer + 1:
                    obj.word_ent.delete(0, 'end')
                    obj.word_ent.insert(0, item[1])
                    break
            else:
                obj.word_ent.delete(0, 'end')

        # mean_ent 조정
        for item in obj.today_mean:
            if item[0] == obj.pointer + 1:
                obj.mean_ent.delete(0, 'end')
                obj.mean_ent.insert(0, item[1])
                break
        else:
            obj.mean_ent.delete(0, 'end')

        selected_scroll_widget(obj)

def start_test(obj, message_lbl, confirm_word_window):
    if not all(btn['bg'] == Color.BEIGE for btn in obj.btn_list):
        show_temp_message(message_lbl, Text_D.WARNING_C[obj.language])
        return

    confirm_word_window.destroy()
    print(obj.today_confirm)
    print(obj.today_mean)
    print(obj.already_know)
    from connector import write_today_word, get_test_data
    if not write_today_word(obj):
        return
    response = get_test_data(obj)
    if not response:
        return
    first = response.get('first')
    second = response.get('second')
    third = response.get('third')
    fourth = response.get('fourth')
    fifth = response.get('fifth')
    
    test_frm = obj.controller.frames['TestFrame']
    test_frm.create_widgets()
    obj.controller.show_frame('TestFrame')


    print(first)
    print(second)
    print(third)
    print(fourth)
    print(fifth)