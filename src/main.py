import os
import tkinter as tk
# TODO: 해상도에 따라 화면이 같게 보이게하기 from ctypes import windll

from dotenv import load_dotenv

from ui import LoginFrame, DailyFrame, TestFrame, ResultFrame
from logic import is_internet_connected, connect_audio, close_audio
from connector import load_ec2_ip, check_server_and_db
from constants import Path, Color, Font_E

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('RoaD')
        self.root.minsize(1000, 728)
        self.root.state('zoomed')

        try:
            self.root.iconbitmap(Path.BI)
        except:
            self.show_overlay('BI road failure')
            return

        self.root.option_add('*Background', Color.GREY)
        self.root.option_add('*Foreground', Color.FONT_DEFAULT)
        self.root.option_add('*TCombobox*Listbox*Background', Color.BEIGE)
        self.root.option_add('*TCombobox*Listbox*Foreground', Color.FONT_DARK)
        self.root.option_add('*TCombobox*Listbox*Font', Font_E.BODY_SMALL)

        if not is_internet_connected():
            self.show_overlay('Internet connection is required.')
            return
        if not check_server_and_db(self):
            return
        
        try:
            self.copy_icon = tk.PhotoImage(file=Path.COPY)
            self.check_icon = tk.PhotoImage(file=Path.CHECK)
            self.speaker_icon = tk.PhotoImage(file=Path.SPEAKER)
            self.next_icon = tk.PhotoImage(file=Path.NEXT)
        except:
            self.show_overlay('Icon road failure')
            return
        
        self.audio = connect_audio()
        self.root.protocol('WM_DELETE_WINDOW', lambda: close_audio(self))

        # 모든 프레임의 부모 프레임
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True)

        # 프레임 초기화 및 저장
        self.frames = {
            F.__name__: F(container, self)
            for F in (LoginFrame, DailyFrame, TestFrame, ResultFrame)
        }
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # 초기 화면을 LoginFrame으로 지정
        self.show_frame('LoginFrame')

    def show_frame(self, frame):
        self.frames[frame].tkraise()

    def show_overlay(self, errormessage):
        '''프로그램이 이용 불가능한 에러 발생 시 오버레이 프레임 띄우는 함수'''
        overlay = tk.Frame(self.root, bg=Color.GREY)
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        tk.Label(overlay, text=errormessage, font=Font_E.TITLE_SMALL).pack(expand=True)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    # TODO: windll.shcore.SetProcessDpiAwareness(1)
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
    load_ec2_ip()
    app = App()
    app.run()