'''GUI 모듈'''
import tkinter as tk
from tkinter import ttk

import logic
import connector
from constants import Color, Font_E, Font_K, Font_J, Text_D

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        body_frm = tk.Frame(self)
        body_frm.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor='center')
        body_frm.bind('<Button-1>', lambda e: body_frm.focus_set())

        # 제목, 버전 라벨
        tk.Label(body_frm, font=Font_E.TITLE, text='RoaD').pack()
        tk.Label(body_frm, font=Font_E.VERSION, text='version 2.0').pack()

        # 로그인 관련 위젯들을 담는 프레임
        bottom_frm = tk.Frame(body_frm, bg=Color.DARK)
        bottom_frm.pack(expand=True)

        # ID 입력창
        username_ent = tk.Entry(
            bottom_frm, bg=Color.GREY, font=Font_E.ENTRY_USERNAME, fg=Color.FONT_USERNAME,
            insertbackground=Color.FONT_USERNAME, justify='center', relief='flat', width=18,
            highlightthickness=1, highlightbackground=Color.GREY, highlightcolor=Color.GREY
        )
        username_ent.insert(0, 'Username')
        username_ent.bind('<FocusIn>', logic.clear_placeholder)
        username_ent.bind('<Return>', lambda e: connector.login(self, username_ent.get()))
        logic.limit_entry_length(username_ent)
        username_ent.pack(padx=90, pady=(60, 50))

        # 로그인 버튼
        tk.Button(
            bottom_frm, bg=Color.GREEN, font=Font_E.BUTTON, text='Log in', width=20,
            command=lambda: connector.login(self, username_ent.get())
        ).pack(pady=(0, 4))

        # 안내, 오류 메시지 라벨
        self.message_lbl = tk.Label(bottom_frm, bg=Color.DARK, font=Font_E.CAPTION)
        self.message_lbl.pack(pady=(0, 5))

        # or 라벨
        tk.Label(bottom_frm, bg=Color.DARK, font=Font_E.SMALL, text='O R').pack(pady=(0, 20))

        # 계정관리 프레임
        account_frm = tk.Frame(bottom_frm, bg=Color.DARK)
        account_frm.grid_columnconfigure(0, weight=1, uniform='col')
        account_frm.grid_columnconfigure(1, weight=1, uniform='col')
        account_frm.pack(pady=(0, 40))

        # 회원가입 라벨
        sign_up_lbl = tk.Label(account_frm, bg=Color.DARK, font=Font_E.ACCOUNT, text='Sign up')
        sign_up_lbl.grid(row=0, column=0, padx=(0, 40))
        sign_up_lbl.bind('<Button-1>', lambda e: self.open_sign_up_window())

        # 계정삭제 라벨
        delete_account_lbl = tk.Label(account_frm, bg=Color.DARK, font=Font_E.ACCOUNT, text='Delete account')
        delete_account_lbl.grid(row=0, column=1, padx=(40, 0))
        delete_account_lbl.bind('<Button-1>', lambda e: self.open_delete_account_window())

    def open_sign_up_window(self):
        sign_up_window = tk.Toplevel(self, bg=Color.DARK)
        sign_up_window.title('Sign up')
        sign_up_window.resizable(False, False)
        sign_up_window.grab_set()
        sign_up_window.bind(
            '<Button-1>', lambda e: sign_up_window.focus_set() if e.widget == sign_up_window else None
        )
        logic.place_window_center(sign_up_window, 480, 580)

        # 제목, 아이디 입력 안내 라벨
        tk.Label(sign_up_window, bg=Color.DARK, font=Font_E.TITLE_SMALL, text='RoaD').pack(pady=30)
        tk.Label(
            sign_up_window, bg=Color.DARK, font=Font_E.BODY_BOLD, text='Enter your ID'
        ).pack(pady=(0, 18))

        # ID 입력창
        username_ent = tk.Entry(
            sign_up_window, bg=Color.GREY, font=Font_E.ENTRY_USERNAME, fg=Color.FONT_USERNAME,
            insertbackground=Color.FONT_USERNAME, justify='center', width=18
        )
        username_ent.insert(0, 'Username')
        username_ent.bind('<FocusIn>', logic.clear_placeholder)
        logic.limit_entry_length(username_ent)
        username_ent.pack(pady=(0, 25))

        # 계정 생성 상세설정 요소를 담는 프레임
        detail_frm = tk.Frame(sign_up_window, bg=Color.DARK)
        detail_frm.pack(pady=(0, 25))

        # 언어 선택
        tk.Label(
            detail_frm, bg=Color.DARK, font=Font_E.BODY, text='Language?'
        ).grid(row=0, column=0, sticky='w', pady=(0, 20))

        language_cbx = ttk.Combobox(
            detail_frm, font=Font_E.BODY_SMALL, state='readonly', values=[' korean', ' japanese'], width=8
        )
        ttk.Style().theme_use('clam')
        language_cbx.set(' korean')
        language_cbx.grid(row=0, column=1, sticky='e', pady=(0, 20))

        # 하루 단어 개수 설정
        tk.Label(
            detail_frm, bg=Color.DARK, font=Font_E.BODY, text='Words per day?'
        ).grid(row=1, column=0, sticky='w', pady=(0, 20))

        dayword_ent = tk.Entry(
            detail_frm, bg=Color.BEIGE, font=Font_E.BODY_SMALL, fg=Color.FONT_DARK,
            insertbackground=Color.FONT_DARK, justify='center', width=3
        )
        dayword_ent.insert(0, '12')
        logic.limit_entry_length(dayword_ent, 2)
        dayword_ent.grid(row=1, column=1, sticky='e', pady=(0, 20))

        # 단어 카테고리
        tk.Label(
            detail_frm, bg=Color.DARK, font=Font_E.BODY, text='What word?'
        ).grid(row=2, column=0, sticky='w', pady=(0, 20))
        category = connector.take_category(self)
        if not category:
            sign_up_window.destroy()
            return
        category = category + [' add yourself']
        category_cbx = ttk.Combobox(
            detail_frm, font=Font_E.BODY_SMALL, state='readonly', values=category, width=11
        )
        ttk.Style().theme_use('clam')
        category_cbx.set(category[0])
        category_cbx.grid(row=2, column=1, sticky='e')

        # 계정 생성 버튼
        tk.Button(
            sign_up_window, bg=Color.GREEN, font=Font_E.BUTTON, text='Sign up', width=20,
            command=lambda: connector.sign_up(
                self, username_ent.get(),
                language_cbx.get(),
                dayword_ent.get(),
                category_cbx.get(),
                message_lbl,
                sign_up_window
            )
        ).pack(pady=(0, 4))

        # 오류메시지
        message_lbl = tk.Label(sign_up_window, bg=Color.DARK, font=Font_E.CAPTION)
        message_lbl.pack()

    def open_delete_account_window(self):
        delete_account_window = tk.Toplevel(self, bg=Color.DARK)
        delete_account_window.title('Delete account')
        delete_account_window.resizable(False, False)
        delete_account_window.grab_set()
        delete_account_window.bind(
            '<Button-1>',
            lambda e: delete_account_window.focus_set() if e.widget == delete_account_window else None
        )
        logic.place_window_center(delete_account_window, 480, 385)

        # 제목, 아이디 입력 안내 라벨
        tk.Label(delete_account_window, bg=Color.DARK, font=Font_E.TITLE_SMALL, text='RoaD').pack(pady=30)
        tk.Label(
            delete_account_window, bg=Color.DARK, font=Font_E.BODY_BOLD, text='Enter ID to Delete'
        ).pack(pady=(0, 20))

        # ID 입력창
        username_ent = tk.Entry(
            delete_account_window, bg=Color.GREY, font=Font_E.ENTRY_USERNAME, fg=Color.FONT_USERNAME,
            insertbackground=Color.FONT_USERNAME, justify='center', width=18
        )
        username_ent.insert(0, 'Username')
        username_ent.bind('<FocusIn>', logic.clear_placeholder)
        logic.limit_entry_length(username_ent)
        username_ent.pack(pady=(0, 32))

        # 계정 삭제 버튼
        tk.Button(
            delete_account_window, bg=Color.BEIGE, font=Font_E.BUTTON,
            fg=Color.FONT_DARK, text='Delete account', width=20,
            command=lambda: connector.check_user_before_delete(
                self, username_ent.get(), message_lbl, delete_account_window
            )
        ).pack(pady=(0, 4))

        # 오류메시지
        message_lbl = tk.Label(delete_account_window, bg=Color.DARK, font=Font_E.CAPTION)
        message_lbl.pack()

    def open_reconfirm_window(self, username, delete_account_window):
        reconfirm_window = tk.Toplevel(delete_account_window, bg=Color.DARK)
        reconfirm_window.title('Reconfirm delete account')
        reconfirm_window.resizable(False, False)
        reconfirm_window.grab_set()
        logic.place_window_center(reconfirm_window, 400, 290)

        # 입력 문구 안내 라벨
        tk.Label(
            reconfirm_window, bg=Color.DARK,
            font=Font_E.BODY, text='To delete, please input'
        ).pack(pady=(25, 0))
        tk.Label(
            reconfirm_window, bg=Color.DARK,
            font=Font_E.BODY_ITALIC, text=f'"delete {username}"'
        ).pack(pady=(10, 15))

        # 입력 문구 입력창
        delete_ent = tk.Entry(
            reconfirm_window, bg=Color.GREY, font=Font_E.ENTRY_DELETE,
            fg=Color.FONT_USERNAME, insertbackground=Color.FONT_USERNAME, justify='center'
        )
        logic.limit_entry_length(delete_ent, len(username) + 7)
        delete_ent.pack(pady=(0, 25))

        # 최종 계정 삭제 버튼
        tk.Button(
            reconfirm_window, bg=Color.BEIGE, font=Font_E.BUTTON,
            fg=Color.FONT_DARK, text='Delete account', width=18,
            command=lambda: connector.delete_account(
                self, delete_ent.get(), username, message_lbl, delete_account_window
            )
        ).pack(pady=(0, 4))

        # 오류메시지
        message_lbl = tk.Label(reconfirm_window, bg=Color.DARK, font=Font_E.CAPTION)
        message_lbl.pack()

class DailyFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bind('<Button-1>', lambda e: self.focus_set())

        self.username = None            # username
        self.language = None            # 선택언어 (K , J)
        self.font = None                # 언어에 따른 폰트 (Font_K, Font_J)
        self.dayword = None             # 오늘의 단어 개수
        self.today_word = []            # 오늘의 단어로 데이터베이스에서 가져온 리스트
        self.pointer = 0                # 화면에 표시할 단어의 인덱스
        self.today_confirm = []         # 오늘의 단어로 확정된 단어리스트
        self.today_mean = []            # 오늘의 단어 뜻 리스트
        self.already_know = []          # 이미 아는 단어 리스트
        self.word_lbl_list = []         # 오른쪽에 표시할 모든 단어라벨
        self.is_add_yourself = False    # add_yourself 인지 아닌지 (True, False)
        self.streak = 0                 # 연속 로그인 횟수(n) or 최초로그인(-2) or 오늘이미 완료(-1)

    def init_user_data(self, username, language, dayword, today_word, is_add_yourself, streak):
        self.username = username
        self.language = language
        self.font = Font_K if self.language == 'K' else Font_J
        self.dayword = dayword
        self.today_word = today_word
        self.is_add_yourself = is_add_yourself
        self.streak = streak

    def create_widgets(self):
        body_frm = tk.Frame(self)
        body_frm.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor='center')
        body_frm.bind('<Button-1>', lambda e: body_frm.focus_set())

        # 제목 라벨
        title_lbl = tk.Label(body_frm, font=self.font.BODY_BIG, anchor='w')
        logic.typing_effect(title_lbl, logic.select_streak_message(self.streak, self.language))
        if self.streak != -1:
            title_lbl.pack()
        else:
            title_lbl.pack_forget()
            title_lbl.pack(expand=True)
            return

        # 중앙 프레임
        center_frm = tk.Frame(body_frm, bg=Color.DARK)
        center_frm.pack(expand=True)

        # 왼쪽 프레임
        left_frm = tk.Frame(center_frm, bg=Color.DARK)
        left_frm.pack(side='left', fill='both', expand=True)
        left_frm.bind('<Button-1>', lambda e: left_frm.focus_set())

        # 진행률 라벨
        self.progress_lbl = tk.Label(
            left_frm, bg=Color.DARK, font=Font_E.BODY_PROGRESS,
            text=f'{len(self.today_confirm)} / {self.dayword}'
        )
        self.progress_lbl.pack(pady=(70, 90))

        if self.is_add_yourself == False:
            # 단어, 아이콘 프레임
            word_frm = tk.Frame(left_frm, bg=Color.DARK)
            word_frm.pack(pady=(0, 90))

            # 영단어 라벨
            self.word_lbl = tk.Label(
                word_frm, bg=Color.DARK, font=Font_E.BODY_WORD, text=self.today_word[self.pointer][1]
            )
            self.word_lbl.pack(side='left')

            # 복사이미지 라벨
            copy_lbl = tk.Label(word_frm, bg=Color.DARK, image=self.controller.copy_icon)
            copy_lbl.pack(side='top', padx=8, pady=(10, 4))
            copy_lbl.bind('<Button-1>', lambda e: logic.copy_word(self, e))

            # 스피커이미지 라벨
            speaker_lbl = tk.Label(word_frm, bg=Color.DARK, image=self.controller.speaker_icon)
            speaker_lbl.pack(side='top')
            speaker_lbl.bind(
                '<Button-1>', lambda e: logic.play_pronunciation(self, self.word_lbl.cget('text'))
            )
        else:
            # 영단어 입력창
            self.word_ent = tk.Entry(
                left_frm, bg=Color.GREY, font=Font_E.BODY_WORD_A, justify='center', relief='flat', width=16,
                highlightthickness=2, highlightbackground=Color.GREY, highlightcolor=Color.GREY
            )
            self.word_ent.pack(pady=(0, 90))
            logic.limit_entry_length(self.word_ent, 20)

        # 뜻 입력창, 버튼 이미 아는 단어 라벨을 담는 프레임
        input_frm = tk.Frame(left_frm, bg=Color.DARK)
        if self.is_add_yourself == False:
            input_frm.pack(padx=55, pady=(0, 10), fill='x')
        else:
            input_frm.pack(padx=55, pady=(20, 10), fill='x')

        if self.is_add_yourself == False:
        # 이미 아는 단어일 경우 라벨
            already_lbl = tk.Label(
                input_frm, bg=Color.DARK, font=self.font.CAPTION, text=Text_D.ALREADY[self.language],
                image=self.controller.next_icon, compound='right'
            )
            already_lbl.bind('<Button-1>', lambda e: logic.on_already_click(
                    self, tip_lbl, record_frm
                )
            )
            already_lbl.grid(row=0, column=0, padx=8, pady=(0, 6), sticky='w')

        # 뜻 입력창
        self.mean_ent = tk.Entry(
            input_frm, bg=Color.GREY, font=self.font.ENTRY, relief='flat', 
            highlightthickness=10, highlightbackground = Color.GREY, highlightcolor = Color.GREY
        )
        if self.language == 'K':
            self.mean_ent.config(width=25)
        else:
            self.mean_ent.config(width=30)
        self.mean_ent.grid(row=1, column=0, padx=(0, 15))
        logic.limit_entry_length(self.mean_ent, 30)
        self.mean_ent.bind('<Return>', lambda e: logic.on_decision_click(
            self, title_lbl, message_lbl, tip_lbl, record_frm
            )
        )

        # 결정 버튼
        tk.Button(
            input_frm, bg=Color.GREEN, font=self.font.ENTRY, text=Text_D.CONFIRM[self.language],
            command=lambda: logic.on_decision_click(
                self, title_lbl, message_lbl, tip_lbl, record_frm
            )
        ).grid(row=1, column=1)

        # 메시지 라벨
        message_lbl = tk.Label(left_frm, bg=Color.DARK, font=self.font.CAPTION)
        if self.is_add_yourself is False:
            message_lbl.pack(pady=(0, 41))
        else:
            message_lbl.pack(pady=(0, 70))

        # 팁 라벨
        tip_lbl = tk.Label(left_frm, bg=Color.DARK, font=self.font.TIP)
        tip_lbl.pack(side='left', padx=20, pady=(0, 20))
        logic.show_daily_tip(self, tip_lbl)

        # 오른쪽 프레임
        right_frm = tk.Frame(center_frm)
        right_frm.pack(side='left', fill='y')

        # Canvas 생성: 스크롤 가능한 영역을 담는 컨테이너
        self.canvas = tk.Canvas(
            right_frm, bg=Color.DEEP, highlightthickness=0, width=250
        )
        self.canvas.pack(side='left', fill='both', expand=True)

        # 수직 스크롤바 생성 및 Canvas와 연결
        scrollbar = tk.Scrollbar(right_frm, command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Canvas 안에 실제 내용(Frame) 생성
        record_frm = tk.Frame(self.canvas, bg=Color.DARK)
        self.canvas.create_window((0, 0), window=record_frm, anchor='nw', width=250)
        record_frm.bind('<Configure>', lambda e: logic.on_configure(e, self.canvas))

        # add yourself가 아닌 경우 첫 단어 오른쪽 리스트에 넣고 시작
        if self.is_add_yourself == False:
            logic.insert_lbl_list(self, record_frm)
            logic.selected_scroll_widget(self)
        else:
            logic.insert_lbl_list_add_yourself(self, record_frm)
            logic.selected_scroll_widget(self)

        # 사전 URL 라벨
        dict_lbl = tk.Label(
            body_frm, font=self.font.CAPTION, text=Text_D.DICT[self.language],
            image=self.controller.copy_icon, compound='right'    
        )
        dict_lbl.bind('<Button-1>', lambda e: logic.copy_url(self, e))
        dict_lbl.pack(side='bottom')
        
    def manual_window(self):
        '''최초 로그인 시 매뉴얼을 보여주는 윈도우'''
        # TODO: self에 Toplevel창 띄워서 UI 설명하기
        pass

    def addyourself_manual_window(self):
        '''add yourself 최초 로그인 시 매뉴얼을 보여주는 윈도우'''
        # TODO: self에 Toplevel창 띄워서 UI 설명하기
        pass

    def word_confirm_window(self):
        '''오늘의 단어를 최종적으로 확인하는 윈도우'''
        # TODO: self에 Toplevel창 띄워서 단어 최종 확인(ok -> testframe, no -> 그냥 창만 종료)
        print(self.today_confirm)
        print(self.today_mean)






class TestFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFF3E0")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # 길이가 긴 텍스트 예시
        text = ("이것은 테스트 화면 예시입니다. 텍스트가 길면 자동으로 줄바꿈이 되도록 "
                "wraplength를 설정했습니다.")
        lbl_text = tk.Label(self, text=text, wraplength=400, justify="center")
        lbl_text.grid(row=0, column=0, columnspan=2, pady=30)

        btn_result = tk.Button(self, text="결과 보기",
                               command=lambda: self.controller.show_frame(ResultFrame))
        btn_result.grid(row=1, column=0, padx=20, pady=10)

        btn_menu = tk.Button(self, text="메뉴로 돌아가기",
                             command=lambda: self.controller.show_frame(DailyFrame))
        btn_menu.grid(row=1, column=1, padx=20, pady=10)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


class ResultFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E8F5E9")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        lbl_title = tk.Label(self, text="결과 화면", font=("Arial", 16, "bold"))
        lbl_title.grid(row=0, column=0, pady=30)

        btn_menu = tk.Button(self, text="메뉴로 돌아가기",
                             command=lambda: self.controller.show_frame(DailyFrame))
        btn_menu.grid(row=1, column=0, pady=10)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)