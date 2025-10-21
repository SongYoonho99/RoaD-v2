import tkinter as tk

from ui import LoginFrame, DailyFrame, TestFrame, ResultFrame, Overframe
from logic import audio_connected, internet_connected
from api_client import server_check
from constants import Path, Color, Font_E

class App:
    '''메인 애플리케이션 클래스'''
    def __init__(self):
        # 메인 Tk 객체
        self.root = tk.Tk()
        self.root.title('RoaD')
        self.root.minsize(1000, 680)
        self.root.state('zoomed')
        self.root.iconbitmap(Path.BI)

        # Tk 옵션 설정
        self.root.option_add('*Background', Color.GREY)
        self.root.option_add('*Foreground', Color.FONT_DEFAULT)
        self.root.option_add('*TCombobox*Listbox*Background', Color.BEIGE)
        self.root.option_add('*TCombobox*Listbox*Foreground', Color.FONT_DARK)
        self.root.option_add('*TCombobox*Listbox*Font', Font_E.BODY_SMALL)

        # 이미지 경로 & 오디오, 인터넷, 서버 체크
        self.copy_icon = tk.PhotoImage(file=Path.COPY)
        self.check_icon = tk.PhotoImage(file=Path.CHECK)
        self.speaker_icon = tk.PhotoImage(file=Path.SPEAKER)
        self.next_icon = tk.PhotoImage(file=Path.NEXT)
        self.audio = audio_connected()
        # TODO: 프로그램종료시 mixer.quit()을 통해 오디오 연결 종료해주는게 좋음
        if not internet_connected():
            self.show_overframe('Internet connection is required.')
            return
        if not server_check(self):
            return

        # 모든 프레임을 담는 컨테이너 생성
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True)

        # 프레임 초기화
        self.frames = {}
        for F in (LoginFrame, DailyFrame, TestFrame, ResultFrame, Overframe):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        # 초기 화면 설정
        self.show_frame(LoginFrame)

    def show_frame(self, frame_class):
        '''특정 프레임을 최상위로 표시'''
        self.frames[frame_class].tkraise()

    def show_overframe(self, errormessage):
        '''서버 에러 발생 시 오버레이 프레임 띄우기'''
        overframe = tk.Frame(self.root, bg=Color.GREY)
        overframe.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 안내 메시지
        tk.Label(
            overframe, text=errormessage, bg=Color.GREY, font=Font_E.TITLE_SMALL
        ).pack(expand=True)

    def run(self):
        '''메인 이벤트 루프 실행'''
        self.root.mainloop()

if __name__ == '__main__':
    app = App()
    app.run()