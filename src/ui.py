'''GUI 모듈'''
import tkinter as tk
from tkinter import ttk

import logic
from api_client import  take_category
from constants import Color, Font_E, Font_K, Font_J, Text_D, Tip

class LoginFrame(tk.Frame):
    '''로그인 화면을 구성하는 프레임'''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bind('<Button-1>', lambda e: self.focus_set())
        self.create_widgets()

    def create_widgets(self):
        '''로그인 화면에 필요한 위젯 생성 및 배치'''
        # 제목, 버전 라벨
        tk.Label(self, font=Font_E.TITLE, text='RoaD').pack(pady=(35, 0))
        tk.Label(self, font=Font_E.VERSION, text='version 2.0').pack()

        # 로그인 관련 위젯들을 담는 프레임
        login_frm = tk.Frame(self, bg=Color.DARK)
        login_frm.pack(expand=True)

        # ID 입력창
        username_ent = tk.Entry(
            login_frm, bg=Color.GREY, font=Font_E.ENTRY_USERNAME, fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY, justify='center'
        )
        username_ent.insert(0, 'Username')
        username_ent.pack(padx=80, pady=(60, 40))
        username_ent.bind('<FocusIn>', logic.clear_placeholder)
        username_ent.bind('<Return>', lambda e: logic.validate_login(self, username_ent.get()))
        logic.limit_entry_length(username_ent)

        # 로그인 버튼
        tk.Button(
            login_frm, bg=Color.GREEN, font=Font_E.BUTTON, text='Log in', width=17,
            command=lambda: logic.validate_login(self, username_ent.get())
        ).pack(pady=(0, 4))

        # 안내, 오류 메시지 라벨
        self.message_lbl = tk.Label(login_frm, bg=Color.DARK, font=Font_E.CAPTION)
        self.message_lbl.pack(pady=(0, 5))

        # or 라벨
        tk.Label(login_frm, bg=Color.DARK, font=Font_E.SMALL, text='O R').pack(pady=(0, 20))

        # 계정관리 프레임
        account_frm = tk.Frame(login_frm, bg=Color.DARK)
        account_frm.grid_columnconfigure(0, weight=1, uniform='col')
        account_frm.grid_columnconfigure(1, weight=1, uniform='col')
        account_frm.pack(pady=(0, 40))

        # 회원가입 라벨
        signup_lbl = tk.Label(account_frm, bg=Color.DARK, font=Font_E.ACCOUNT, text='Sign up')
        signup_lbl.grid(row=0, column=0, padx=(0, 30))
        signup_lbl.bind('<Button-1>', lambda e: self.signup_window())

        # 계정삭제 라벨
        delaccount_lbl = tk.Label(account_frm, bg=Color.DARK, font=Font_E.ACCOUNT, text='Delete account')
        delaccount_lbl.grid(row=0, column=1, padx=(30, 0))
        delaccount_lbl.bind('<Button-1>', lambda e: self.delaccount_window())

    def signup_window(self):
        '''계정 생성 창 위젯 생성 및 배치'''
        signup_window = tk.Toplevel(self, bg=Color.DARK)
        signup_window.title('Sign Up')
        signup_window.resizable(False, False)
        signup_window.grab_set()
        signup_window.bind(
            '<Button-1>', lambda e: signup_window.focus_set() if e.widget == signup_window else None
        )
        logic.center_window(signup_window, 480, 580)

        # 제목, 아이디 입력 라벨
        tk.Label(signup_window, bg=Color.DARK, font=Font_E.TITLE_SMALL, text='RoaD').pack(pady=30)
        tk.Label(
            signup_window, bg=Color.DARK, font=Font_E.BODY_BOLD, text='Enter your ID'
        ).pack(pady=(0, 18))

        # ID 입력창
        username_ent = tk.Entry(
            signup_window, bg=Color.GREY, font=Font_E.ENTRY_USERNAME, fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY, justify='center'
        )
        username_ent.insert(0, 'Username')
        username_ent.pack(pady=(0, 25))
        username_ent.bind('<FocusIn>', logic.clear_placeholder)
        logic.limit_entry_length(username_ent)

        # 계정 생성 상세설정 요소를 담는 프레임
        detail_frm = tk.Frame(signup_window, bg=Color.DARK)
        detail_frm.pack(pady=(0, 25))

        # 언어 선택 라벨
        tk.Label(
            detail_frm, bg=Color.DARK, font=Font_E.BODY, text='Language?'
        ).grid(row=0, column=0, sticky='w', pady=(0, 20))

        # 언어 선택 콤보박스
        language_cbx = ttk.Combobox(
            detail_frm, font=Font_E.BODY_SMALL, state='readonly', values=[' korean', ' japanese'], width=8
        )
        ttk.Style().theme_use('clam')
        language_cbx.set(' korean')
        language_cbx.grid(row=0, column=1, sticky='e', pady=(0, 20))

        # 하루 단어 개수 설정 라벨
        tk.Label(
            detail_frm, bg=Color.DARK, font=Font_E.BODY, text='Words per day?'
        ).grid(row=1, column=0, sticky='w', pady=(0, 20))

        # 하루 단어 개수 설정 입력창
        dayword_ent = tk.Entry(
            detail_frm, bg=Color.BEIGE, font=Font_E.BODY_SMALL, fg=Color.FONT_DARK,
            insertbackground=Color.FONT_DARK, justify='center', width=3
        )
        dayword_ent.insert(0, '12')
        dayword_ent.grid(row=1, column=1, sticky='e', pady=(0, 20))
        logic.limit_entry_length(dayword_ent, 2)

        # 단어 카테고리 라벨
        tk.Label(
            detail_frm, bg=Color.DARK, font=Font_E.BODY, text='What word?'
        ).grid(row=2, column=0, sticky='w', pady=(0, 20))

        # 언어 선택 콤보박스
        category = take_category(self)
        category = category + [' add yourself']
        category_cbx = ttk.Combobox(
            detail_frm, font=Font_E.BODY_SMALL, state='readonly',
            values=category, width=11
        )
        ttk.Style().theme_use('clam')
        category_cbx.set(category[0])
        category_cbx.grid(row=2, column=1, sticky='e')

        # 계정 생성 버튼
        tk.Button(
            signup_window, bg=Color.GREEN, font=Font_E.BUTTON, text='Sign up', width=17,
            command=lambda: logic.validate_signup(
                self,
                username_ent.get(),
                language_cbx.get(),
                dayword_ent.get(),
                category_cbx.get(),
                signupmessage_lbl,
                signup_window
            )
        ).pack(pady=(0, 4))

        # 오류메시지
        signupmessage_lbl = tk.Label(signup_window, bg=Color.DARK, font=Font_E.CAPTION)
        signupmessage_lbl.pack()

    def delaccount_window(self):
        '''계정 삭제 창 위젯 생성 및 배치'''
        delaccount_window = tk.Toplevel(self, bg=Color.DARK)
        delaccount_window.title('Delete Account')
        delaccount_window.resizable(False, False)
        delaccount_window.grab_set()
        delaccount_window.bind(
            '<Button-1>', lambda e: delaccount_window.focus_set() if e.widget == delaccount_window else None
        )
        logic.center_window(delaccount_window, 480, 385)

        # 제목, 아이디 입력 라벨
        tk.Label(delaccount_window, bg=Color.DARK, font=Font_E.TITLE_SMALL, text='RoaD').pack(pady=30)
        tk.Label(
            delaccount_window, bg=Color.DARK, font=Font_E.BODY_BOLD, text='Enter ID to Delete'
        ).pack(pady=(0, 18))

        # ID 입력창
        username_ent = tk.Entry(
            delaccount_window, bg=Color.GREY, font=Font_E.ENTRY_USERNAME, fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY, justify='center'
        )
        username_ent.insert(0, 'Username')
        username_ent.pack(pady=(0, 40))
        username_ent.bind('<FocusIn>', logic.clear_placeholder)
        logic.limit_entry_length(username_ent)

        # 계정 삭제 버튼
        tk.Button(
            delaccount_window, bg=Color.BEIGE, font=Font_E.BUTTON,
            fg=Color.FONT_DARK, text='Delect Account', width=17,
            command=lambda: logic.delaccount_check_user(
                self,
                username_ent.get(),
                delmessage_lbl,
                delaccount_window
            )
        ).pack(pady=(0, 4))

        # 오류메시지
        delmessage_lbl = tk.Label(delaccount_window, bg=Color.DARK, font=Font_E.CAPTION)
        delmessage_lbl.pack()

    def delaccount_reconfirm_window(self, username, delaccount_window):
        '''계정삭제 최종확인 창'''
        reconfirm_window = tk.Toplevel(delaccount_window, bg=Color.DARK)
        reconfirm_window.title('Delete Account Reconfirm')
        reconfirm_window.resizable(False, False)
        reconfirm_window.grab_set()
        reconfirm_window.bind(
            '<Button-1>', lambda e: reconfirm_window.focus_set() if e.widget == reconfirm_window else None
        )
        logic.center_window(reconfirm_window, 400, 280)

        # 입력 문구 안내 라벨
        tk.Label(
            reconfirm_window, bg=Color.DARK, font=Font_E.BODY, text='To delete, please input'
        ).pack(pady=(25, 0))
        tk.Label(
            reconfirm_window, bg=Color.DARK, font=Font_E.BODY_ITALIC,
            text=f'"delete {username}"'
        ).pack(pady=(10, 15))

        # 입력 문구 입력창
        delete_ent = tk.Entry(
            reconfirm_window, bg=Color.GREY, font=Font_E.ENTRY_USERNAME, fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY, justify='center'
        )
        delete_ent.pack(pady=(0, 25))

        # 최종 계정 삭제 버튼
        tk.Button(
            reconfirm_window, bg=Color.BEIGE, font=Font_E.BUTTON,
            fg=Color.FONT_DARK, text='Delete', width=10,
            command=lambda: logic.validate_delaccount(
                self, delete_ent.get(), username, delmessage_lbl, delaccount_window
            )
        ).pack(pady=(0, 4))

        # 오류메시지
        delmessage_lbl = tk.Label(reconfirm_window, bg=Color.DARK, font=Font_E.CAPTION)
        delmessage_lbl.pack()

class DailyFrame(tk.Frame):
    '''오늘의 단어를 추가하는 프레임'''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bind('<Button-1>', lambda e: self.focus_set())

        # 변수 초기화
        self.username = None    # username
        self.language = None    # 선택언어 (K , J)
        self.font = None        # 언어폰트 (Font_K, Font_J)
        self.dayword = None     # 오늘의 단어 개수
        self.today_word = []    # 오늘의 단어로 데이터베이스에서 가져온 리스트
        self.pointer = 0        # 현재 화면에 표시할 단어의 번호
        self.today_confirm = [] # 오늘의 단어로 확정된 단어리스트
        self.today_mean = []    # 오늘의 단어 뜻 리스트
        self.already_know = []  # 이미 아는 단어 리스트
        self.word_lbl_list = [] # 오른쪽에 표시할 모든 단어
        self.addbool = None     # add_yourself 인지 아닌지 (True, False)
        self.streak = 0         # 연속 로그인 횟수(n) or 최초로그인(-2) or 오늘이미 완료(-1)

    def set_data(self, username, language, dayword, today_word, addbool, streak):
        '''로그인시 로그인 정보롤 데이터 초기화'''
        self.username = username
        self.language = language
        self.font = Font_K if self.language == 'K' else Font_J  # 폰트설정 편하게 하기위한 변수
        self.dayword = dayword
        self.today_word = today_word
        self.addbool = addbool
        self.streak = streak

    def create_widgets(self):
        '''오늘의 단어 화면에 필요한 위젯 생성 및 배치'''
        # 최초로그인 or 연속로그인상태 or 오늘이미 완료 라벨
        title_lbl = tk.Label(self, font=self.font.BODY_BIG, anchor='w')
        title_lbl.pack(pady=40)
        logic.type_writer(title_lbl, logic.streak(self.streak, self.language))

        # 중앙 프레임
        center_frm = tk.Frame(self, bg=Color.DARK)
        center_frm.pack(padx=150, expand=True, fill='both')

        # 왼쪽 프레임
        left_frm = tk.Frame(center_frm, bg=Color.DARK)
        left_frm.pack(side='left', fill='both', expand=True)
        left_frm.bind('<Button-1>', lambda e: left_frm.focus_set())

        # 진행률라벨
        self.progress_lbl = tk.Label(
            left_frm, bg=Color.DARK, font=Font_E.BODY_BIG_BOLD,
            text=f'{len(self.today_confirm)} / {self.dayword}'
        )
        self.progress_lbl.pack(pady=60)

        # add yourself 가 아닌 경우
        if self.addbool == False:
            # 단어, 아이콘 프레임
            word_frm = tk.Frame(left_frm, bg=Color.DARK)
            word_frm.pack(pady=(15, 45))

            # 영단어 라벨
            self.word_lbl = tk.Label(
                word_frm, bg=Color.DARK, font=Font_E.BODY_BIG_BOLD,
                text=self.today_word[self.pointer][1]
            )
            self.word_lbl.pack(side='left')

            # 복사이미지 라벨
            copy_lbl = tk.Label(word_frm, bg=Color.DARK, image=self.controller.copy_icon)
            copy_lbl.pack(side='top', padx= 10, pady=(0, 2))
            copy_lbl.bind('<Button-1>', lambda e: logic.copy_word(self, e))

            # 스피커이미지 라벨
            speaker_lbl = tk.Label(word_frm, bg=Color.DARK, image=self.controller.speaker_icon)
            speaker_lbl.pack(side='top')
            speaker_lbl.bind(
                '<Button-1>', lambda e: logic.play_pronunciation(self, self.word_lbl.cget('text'))
            )
        # add yourself 인 경우
        else:
            # 단어 입력창
            self.word_ent = tk.Entry(
                left_frm, bg=Color.GREY, font=Font_E.BODY_BOLD, justify='center',
                relief='flat', width=25, highlightthickness=10,
                highlightbackground = Color.GREY, highlightcolor = Color.GREY
            )
            self.word_ent.pack(pady=(15, 85))
            logic.limit_entry_length(self.word_ent, 20)

        # 뜻 입력창, 버튼 이미 아는 단어 라벨을 담는 프레임
        input_frm = tk.Frame(left_frm, bg=Color.DARK)
        input_frm.pack(pady=(0, 6))

        if self.addbool == False:
        # 이미 아는 단어일 경우 라벨
            already_lbl = tk.Label(
                input_frm, bg=Color.DARK, font=self.font.CAPTION, text=Text_D.ALREADY[self.language],
                image=self.controller.next_icon, compound='right'
            )
            already_lbl.bind('<Button-1>', lambda e: logic.already_know_word(
                    self, tip_lbl, record_frm
                )
            )
            already_lbl.grid(row=0, column=0, padx=13, pady=(0, 6), sticky='w')

        # 뜻 입력창
        self.mean_ent = tk.Entry(
            input_frm, bg=Color.GREY, font=self.font.ENTRY,
            relief='flat', width=25, highlightthickness=10,
            highlightbackground = Color.GREY, highlightcolor = Color.GREY
        )
        self.mean_ent.grid(row=1, column=0, padx=15)
        logic.limit_entry_length(self.mean_ent, 50)
        self.mean_ent.bind('<Return>', lambda e: logic.daily_confirm(
            self, title_lbl, message_lbl, tip_lbl, record_frm
            )
        )

        # 결정 버튼
        tk.Button(
            input_frm, bg=Color.GREEN, font=self.font.ENTRY,
            text=Text_D.CONFIRM[self.language],
            command=lambda: logic.daily_confirm(
                self, title_lbl, message_lbl, tip_lbl, record_frm
            )
        ).grid(row=1, column=1, padx=15)

        # 메시지 라벨
        message_lbl = tk.Label(left_frm, bg=Color.DARK, font=self.font.CAPTION)
        message_lbl.pack(pady=(0, 20))

        # 팁 라벨
        tip_lbl = tk.Label(left_frm, bg=Color.DARK, font=self.font.CAPTION)
        tip_lbl.pack(side='left', padx=20)
        logic.show_random_tip(self, tip_lbl)

        # 오른쪽 프레임
        right_frm = tk.Frame(center_frm)
        right_frm.pack(side='left', fill='y')

        # Canvas 생성: 스크롤 가능한 영역을 담는 컨테이너
        canvas = tk.Canvas(
            right_frm, bg=Color.DEEP, highlightbackground = Color.DARK, width=200
        )
        canvas.pack(side='left', fill='both', expand=True)
        canvas.bind_all('<MouseWheel>', lambda e: logic.on_mousewheel(e, canvas))

        # 수직 스크롤바 생성 및 Canvas와 연결
        scrollbar = tk.Scrollbar(right_frm, command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Canvas 안에 실제 내용(Frame) 생성
        record_frm = tk.Frame(canvas, bg=Color.DARK)
        canvas.create_window((0, 0), window=record_frm, anchor='nw', width=200)
        record_frm.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # add yourself가 아닌 경우 첫 단어 오른쪽 리스트에 넣고 시작
        if self.addbool == False:
            logic.insert_word_lbl_list(self, record_frm)
            logic.selected_scroll_widget(self)
        else:
            logic.insert_word_lbl_list_addbool(self, record_frm)
            logic.selected_scroll_widget(self)

        # 사전 URL 라벨
        dict_lbl = tk.Label(
            self, font=self.font.CAPTION, text=Text_D.DICT[self.language],
            image=self.controller.copy_icon, compound='right'    
        )
        dict_lbl.bind('<Button-1>', lambda e: logic.copy_dict(self, e))
        dict_lbl.pack(side='left', padx=160, pady=(6, 54))
        
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