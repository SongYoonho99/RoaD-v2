'''GUI 모듈'''
import tkinter as tk
from tkinter import ttk

import logic
import connector
from constants import Path, Color, Font_E, Font_K, Font_J, Text_D, Text_T

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
            bottom_frm, bg=Color.GREY, font=Font_E.ENTRY_USERNAME, fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY, justify='center', relief='flat', width=18,
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
            '<Button-1>',
            lambda e: sign_up_window.focus_set() if e.widget == sign_up_window else None
        )
        logic.place_window_center(sign_up_window, 480, 580)

        # 제목, 아이디 입력 안내 라벨
        tk.Label(sign_up_window, bg=Color.DARK, font=Font_E.TITLE_SMALL, text='RoaD').pack(pady=30)
        tk.Label(
            sign_up_window, bg=Color.DARK, font=Font_E.BODY_BOLD, text='Enter your ID'
        ).pack(pady=(0, 18))

        # ID 입력창
        username_ent = tk.Entry(
            sign_up_window, bg=Color.GREY, font=Font_E.ENTRY_USERNAME, fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY, justify='center', width=18
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
            delete_account_window, bg=Color.GREY, font=Font_E.ENTRY_USERNAME, fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY, justify='center', width=18
        )
        username_ent.insert(0, 'Username')
        username_ent.bind('<FocusIn>', logic.clear_placeholder)
        username_ent.bind('<Return>', lambda e: connector.check_user_before_delete(
                self, username_ent.get(), message_lbl, delete_account_window
            )
        )
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
        reconfirm_window.bind(
            '<Button-1>',
            lambda e: reconfirm_window.focus_set() if e.widget == reconfirm_window else None
        )
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
            fg=Color.FONT_ENTRY, insertbackground=Color.FONT_ENTRY, justify='center'
        )
        delete_ent.bind('<Return>', lambda e: connector.delete_account(
                self, delete_ent.get(), username, message_lbl, delete_account_window
            )
        )
        logic.limit_entry_length(delete_ent, len(username) + 7)
        delete_ent.pack(pady=(0, 25))
        delete_ent.focus()

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

    def init_data(self, username, language, dayword, today_word, is_add_yourself, streak):
        self.username = username
        self.language = language
        self.font = Font_K if self.language == 'K' else Font_J
        self.dayword = dayword
        self.today_word = today_word    # 데이터베이스에서 후보로 가져온 단어 리스트
        self.pointer = 0                # 화면에 표시할 today_word의 인덱스
        self.today_confirm = []         # 오늘의 단어로 확정된 단어리스트
        self.already_know = []          # 이미 아는 단어 리스트
        self.word_lbl_list = []         # 오른쪽에 표시할 모든 단어라벨
        self.is_add_yourself = is_add_yourself
        self.streak = streak
        self.btn_list = []              # confirm_word_window에서 사용하는 버튼 리스트
        self.lbl_list = []              # confirm_word_window에서 사용하는 라벨 리스트
        self.ent_list = []              # confirm_word_window에서 사용하는 엔트리 리스트

    def create_widgets(self):
        body_frm = tk.Frame(self)
        body_frm.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor='center')
        body_frm.bind('<Button-1>', lambda e: body_frm.focus_set())

        # 제목 라벨
        title_lbl = tk.Label(body_frm, font=self.font.BODY_BIG, anchor='w')
        logic.typing_effect(title_lbl, logic.select_streak_message(self.streak, self.language))
        if self.streak is not True:
            title_lbl.pack()
        else: # 오늘 이미 했을 경우
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
                word_frm, bg=Color.DARK, font=Font_E.BODY_WORD, text=self.today_word[self.pointer]
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
            self.word_ent.bind('<Return>', lambda e: logic.on_decision_click(
                    self, title_lbl, message_lbl, tip_lbl, record_frm
                )
            )
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
                    self, tip_lbl, message_lbl, record_frm
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
        self.mean_ent.grid(row=1, column=0, padx=(0, 18))
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
        
    def open_manual_window(self):
        '''최초 로그인 시 매뉴얼을 보여주는 윈도우'''
        try:
            if self.language == 'K':
                manual = tk.PhotoImage(file=Path.MANUAL_K)
            else:
                manual = tk.PhotoImage(file=Path.MANUAL_J)
            self.page = 0
        except:
            self.controller.show_overlay('Icon road failure')
            return
        
        manual_window = tk.Toplevel(self)
        manual_window.title(Text_D.MANUAL_TITLE[self.language])
        manual_window.resizable(False, False)
        logic.place_window_center(manual_window, 900, 720)

        manual_lbl = tk.Label(manual_window, image=manual)
        manual_lbl.image = manual
        manual_lbl.place(x=(900 - manual.width()) // 2 - 5)

        # 2 페이지
        square_progress = tk.PhotoImage(file=Path.SQUARE_PROGRESS)
        square_progress_lbl = tk.Label(manual_window, image=square_progress)
        square_progress_lbl.image = square_progress

        # 3 페이지
        square_mean = tk.PhotoImage(file=getattr(Path, f'SQUARE_MEAN_{self.language}'))
        square_mean_lbl = tk.Label(manual_window, image=square_mean)
        square_mean_lbl.image = square_mean
        square_dict = tk.PhotoImage(file=getattr(Path, f'SQUARE_DICT_{self.language}'))
        square_dict_lbl = tk.Label(manual_window, image=square_dict)
        square_dict_lbl.image = square_dict

        # 4 페이지
        square_know = tk.PhotoImage(file=getattr(Path, f'SQUARE_KNOW_{self.language}'))
        square_know_lbl = tk.Label(manual_window, image=square_know)
        square_know_lbl.image = square_know

        # 5 페이지
        square_right = tk.PhotoImage(file=getattr(Path, f'SQUARE_RIGHT_{self.language}'))
        square_right_lbl = tk.Label(manual_window, image=square_right)
        square_right_lbl.image = square_right

        message_lbl = tk.Label(
            manual_window, bg=Color.DEEP, font=self.font.BODY_SMALL, fg=Color.FONT_RED,
            text=Text_D.MANUAL_1[self.language]
        )
        message_lbl.place(relx=0.5, rely=1.0, anchor='s', y=-75)

        next_btn = tk.Button(
            manual_window, bg=Color.GREEN, font=self.font.BODY_SMALL,
            text=Text_D.NEXT[self.language],
            command=lambda: logic.next_manual_page(
                self, message_lbl, square_progress_lbl, square_mean_lbl, square_dict_lbl,
                square_know_lbl, square_right_lbl, next_btn, manual_window
            )
        )
        next_btn.place(relx=0.5, rely=1.0, anchor='s', y=-10)

    def open_add_yourself_manual_window(self):
        '''add yourself 최초 로그인 시 매뉴얼을 보여주는 윈도우'''
        try:
            if self.language == 'K':
                manual = tk.PhotoImage(file=Path.MANUAL_ADD_K)
            else:
                manual = tk.PhotoImage(file=Path.MANUAL_ADD_J)
            self.page = 0
        except:
            self.controller.show_overlay('Icon road failure')
            return
        
        manual_window = tk.Toplevel(self)
        manual_window.title(Text_D.MANUAL_TITLE[self.language])
        manual_window.resizable(False, False)
        logic.place_window_center(manual_window, 900, 720)

        manual_lbl = tk.Label(manual_window, image=manual)
        manual_lbl.image = manual
        manual_lbl.place(x=(900 - manual.width()) // 2 - 5)

        # 2 페이지
        square_progress = tk.PhotoImage(file=Path.SQUARE_PROGRESS)
        square_progress_lbl = tk.Label(manual_window, image=square_progress)
        square_progress_lbl.image = square_progress

        # 3 페이지
        square_word = tk.PhotoImage(file=getattr(Path, f'SQUARE_WORD'))
        square_word_lbl = tk.Label(manual_window, image=square_word)
        square_word_lbl.image = square_word
        square_mean = tk.PhotoImage(file=getattr(Path, f'SQUARE_MEAN_ADD_{self.language}'))
        square_mean_lbl = tk.Label(manual_window, image=square_mean)
        square_mean_lbl.image = square_mean

        # 4 페이지
        square_right_add = tk.PhotoImage(file=Path.SQUARE_RIGHT_ADD)
        square_right_add_lbl = tk.Label(manual_window, image=square_right_add)
        square_right_add_lbl.image = square_right_add

        message_lbl = tk.Label(
            manual_window, bg=Color.DEEP, font=self.font.BODY_SMALL, fg=Color.FONT_RED,
            text=Text_D.MANUAL_1[self.language]
        )
        message_lbl.place(relx=0.5, rely=1.0, anchor='s', y=-75)

        next_btn = tk.Button(
            manual_window, bg=Color.GREEN, font=self.font.BODY_SMALL,
            text=Text_D.NEXT[self.language],
            command=lambda: logic.next_manual_page_add(
                self, message_lbl, square_progress_lbl, square_word_lbl, square_mean_lbl,
                square_right_add_lbl, next_btn, manual_window
            )
        )
        next_btn.place(relx=0.5, rely=1.0, anchor='s', y=-10)

    def open_confirm_word_window(self):
        confirm_word_window = tk.Toplevel(self)
        confirm_word_window.title(Text_D.TITLE_CONFIRM_WORD_WINDOW[self.language])
        confirm_word_window.resizable(False, False)
        confirm_word_window.grab_set()
        confirm_word_window.bind(
            '<Button-1>',
            lambda e: confirm_word_window.focus_set() if e.widget == confirm_word_window else None
        )
        logic.place_window_center(confirm_word_window, 700, 635)
        confirm_word_window.protocol('WM_DELETE_WINDOW', lambda: None)

        body_frm = tk.Frame(confirm_word_window)
        body_frm.pack(padx=30, pady=(30, 20), fill='both', expand=True)

        # Canvas 생성: 스크롤 가능한 영역을 담는 컨테이너
        canvas = tk.Canvas(body_frm, bg=Color.DARK, highlightthickness=0)
        canvas.bind('<MouseWheel>', lambda e: logic.on_mousewheel(e, canvas))
        canvas.pack(side='left', fill='both', expand=True)

        # 수직 스크롤바 생성 및 Canvas와 연결
        scrollbar = tk.Scrollbar(body_frm, command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Canvas 안에 실제 내용(Frame) 생성
        main_frm = tk.Frame(canvas, bg=Color.DARK)
        canvas.create_window((0, 0), window=main_frm, anchor='nw')
        main_frm.bind('<Configure>', lambda e: logic.on_configure(e, canvas))

        # 스크롤바 내부 위젯 배치
        for i in range(len(self.today_confirm)):
            # 영단어 라벨
            word_lbl = tk.Label(
                main_frm, bg=Color.DARK, font = Font_E.BODY, anchor='w',
                highlightthickness=5, highlightbackground=Color.DARK,
                text=f'{i+1}. {self.today_confirm[i][0]}'
            )
            word_lbl.bind('<MouseWheel>', lambda e: logic.on_mousewheel(e, canvas))
            word_lbl.grid(row=i, column=0, sticky='ew')

            # 버튼
            btn = tk.Button(
                main_frm, bg=Color.BEIGE, font=self.font.MODIFY_BUTTON, fg=Color.FONT_DARK,
                text=Text_D.MODYFICATION[self.language],
                command=lambda n=i: logic.change_mean(self, n)
            )
            btn.bind('<MouseWheel>', lambda e: logic.on_mousewheel(e, canvas))
            btn.grid(row=i, column=1, padx=(10, 20), pady=4, sticky='ew')
            self.btn_list.append(btn)

            # 뜻 라벨
            mean_lbl = tk.Label(
                main_frm, bg=Color.DARK, font=self.font.BODY, anchor='w', text=self.today_confirm[i][1]
            )
            mean_lbl.bind('<MouseWheel>', lambda e: logic.on_mousewheel(e, canvas))
            mean_lbl.grid(row=i, column=2, sticky='ew')
            self.lbl_list.append(mean_lbl)

            # 뜻 엔트리
            mean_ent = tk.Entry(
                main_frm, bg=Color.GREY, font=self.font.ENTRY_CONFIRM, insertbackground=Color.FONT_ENTRY,
                highlightthickness=5, highlightbackground=Color.GREY, highlightcolor=Color.GREY, relief='flat'
            )
            mean_ent.insert(0, self.today_confirm[i][1])
            mean_ent.bind('<Return>', lambda e, n=i: logic.change_mean(self, n))
            mean_ent.bind('<MouseWheel>', lambda e: logic.on_mousewheel(e, canvas))
            self.ent_list.append(mean_ent)

        tk.Button(
            confirm_word_window, bg=Color.GREEN, font=self.font.CONFIRM_BUTTON,
            text=Text_D.START_TEST[self.language],
            command=lambda: logic.start_test(self, message_lbl, confirm_word_window)
        ).pack(pady=(0, 4))
        message_lbl = tk.Label(
            confirm_word_window, bg=Color.GREY, fg=Color.FONT_RED, font=self.font.CAPTION_SMALL,
        )
        message_lbl.pack(pady=(0, 8))

class TestFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    def init_data(
            self, username, language, is_add_yourself, today_confirm,
            first, second, third, fourth, fifth, streak
        ):
        self.username = username
        self.language = language
        self.font = Font_K if self.language == 'K' else Font_J
        self.is_add_yourself = is_add_yourself
        self.today_confirm = today_confirm
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
        self.fifth = fifth
        self.streak = streak

    def create_widgets(self):
        body_frm = tk.Frame(self)
        body_frm.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor='center')
        body_frm.bind('<Button-1>', lambda e: body_frm.focus_set())

        # 제목 라벨
        tk.Label(body_frm, font=self.font.BODY_BIG, anchor='w', text=Text_T.TITLE[self.language]).pack()

        # 중앙 프레임
        center_frm = tk.Frame(body_frm, bg=Color.DARK)
        center_frm.pack(expand=True)

        # 왼쪽 프레임
        left_frm = tk.Frame(center_frm, bg=Color.DARK)
        left_frm.pack(side='left', fill='both', expand=True)
        left_frm.bind('<Button-1>', lambda e: left_frm.focus_set())

        # 단어 정보 라벨
        date_lbl = tk.Label(left_frm, bg=Color.DARK, font=self.font.TIP, text='10/27에 외운 단어(3번째 복습)')
        date_lbl.pack(padx=20, pady=(20, 36), anchor='w')

        # 진행률 라벨
        self.progress_lbl = tk.Label(left_frm, bg=Color.DARK, font=Font_E.BODY_PROGRESS, text='3 / 60')
        self.progress_lbl.pack(pady=(0, 70))

        # 영단어와 스피커를 담는 프레임
        word_frm = tk.Frame(left_frm, bg=Color.DARK)
        word_frm.pack(pady=(0, 70))

        # 영단어 라벨
        self.word_lbl = tk.Label(
            word_frm, bg=Color.DARK, font=Font_E.BODY_WORD, text='label'
        )
        self.word_lbl.pack(side='left')

        # 스피커이미지 라벨
        speaker_lbl = tk.Label(word_frm, bg=Color.DARK, image=self.controller.speaker_icon)
        speaker_lbl.pack(side='left', padx=10,  fill='y', anchor='center')
        speaker_lbl.bind(
            '<Button-1>', lambda e: logic.play_pronunciation(self, self.word_lbl.cget('text'))
        )

        # 뜻 입력창 프레임
        self.input_frm = tk.Frame(left_frm, bg=Color.DARK)
        # self.input_frm.pack(padx=55, pady=(55, 120))

        # 뜻 입력창
        mean_ent = tk.Entry(
            self.input_frm, bg=Color.GREY, font=self.font.ENTRY, relief='flat', 
            highlightthickness=10, highlightbackground = Color.GREY, highlightcolor = Color.GREY
        )
        if self.language == 'K':
            mean_ent.config(width=25)
        else:
            mean_ent.config(width=30)
        mean_ent.grid(row=1, column=0, padx=(0, 18))
        logic.limit_entry_length(mean_ent, 30)

        # 결정 버튼
        tk.Button(
            self.input_frm, bg=Color.GREEN, font=self.font.ENTRY, text=Text_D.CONFIRM[self.language],
        ).grid(row=1, column=1)

        # 채점결과 프레임
        self.review_frm = tk.Frame(left_frm, bg=Color.DARK)
        self.review_frm.pack(padx=25, pady=(0, 37))

        # 채점 결과 라벨
        tk.Label(
            self.review_frm, bg=Color.DARK, font=self.font.REVIEW,
            text=Text_T.RESULT[self.language]
        ).grid(row=0, column=0, pady=5, sticky='w')
        tk.Label(
            self.review_frm, bg=Color.DARK, font=self.font.REVIEW, text=':'
        ).grid(row=0, column=1, padx=5, pady=5)
        self.result_lbl = tk.Label(
            self.review_frm, bg=Color.DARK, font=Font_E.REVIEW, fg=Color.FONT_RED, text='X'
        )
        self.result_lbl.grid(row=0, column=2, padx=(0, 454), pady=5, sticky='w')

        # 정오답, 유저의 입력 라벨
        tk.Label(
            self.review_frm, bg=Color.DARK, font=self.font.REVIEW,
            text=Text_T.USER_ANSWER[self.language]
        ).grid(row=1, column=0, pady=5, sticky='w')
        tk.Label(
            self.review_frm, bg=Color.DARK, font=self.font.REVIEW, text=':'
        ).grid(row=1, column=1, padx=5, pady=5)
        self.user_answer_lbl = tk.Label(
            self.review_frm, bg=Color.DARK, font=self.font.REVIEW, text='레벨'
        )
        self.user_answer_lbl.grid(row=1, column=2, pady=5, sticky='w')

        # 모범답안 라벨
        tk.Label(
            self.review_frm, bg=Color.DARK, font=self.font.REVIEW,
            text=Text_T.MODEL_ANSWER[self.language]
        ).grid(row=2, column=0, pady=5, sticky='w')
        tk.Label(
            self.review_frm, bg=Color.DARK, font=self.font.REVIEW, text=':'
        ).grid(row=2, column=1, padx=5, pady=5)
        self.model_answer_lbl = tk.Label(
            self.review_frm, bg=Color.DARK, font=self.font.REVIEW,
            text='가나다라마바'
        )
        self.model_answer_lbl.grid(row=2, column=2, pady=5, sticky='w')

        # 코멘트
        tk.Label(
            self.review_frm, bg=Color.DARK, font=self.font.REVIEW,
            text=Text_T.COMMENT[self.language]
        ).grid(row=3, column=0, pady=5, sticky='w')
        tk.Label(
            self.review_frm, bg=Color.DARK, font=self.font.REVIEW, text=':'
        ).grid(row=3, column=1, padx=5, pady=5)
        self.comment_lbl = tk.Label(
            self.review_frm, bg=Color.DARK, font=self.font.REVIEW,
            text='정확합니다.'
        )
        self.comment_lbl.grid(row=3, column=2, pady=5, sticky='w')

        # 팁 라벨
        tip_lbl = tk.Label(left_frm, bg=Color.DARK, font=self.font.TIP)
        tip_lbl.pack(side='left', padx=20, pady=(0, 20))
        logic.show_test_tip(self, tip_lbl)

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

        # print(self.first, self.second, self.third, self.fourth, self.fifth)

    def set_init_widgets(self):
        pass
 






class ResultFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    def create_widgets(self):
        pass