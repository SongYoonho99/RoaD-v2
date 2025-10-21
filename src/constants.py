'''상수 모듈'''
class Path:
    '''데이터파일 상대경로 클래스'''
    import os

    BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

    BI = os.path.join(BASE_DIR, 'BI.ico')
    COPY = os.path.join(BASE_DIR, 'copy.png')
    CHECK = os.path.join(BASE_DIR, 'check.png')
    SPEAKER = os.path.join(BASE_DIR, 'speaker.png')
    NEXT = os.path.join(BASE_DIR, 'next.png')

class Color:
    '''UI에서 사용하는 색상 상수 클래스'''
    GREY = '#3C3A38'
    DARK = '#262421'
    GREEN = '#5d9948'
    BEIGE = '#D9D6D2'
    DEEP = '#2a2a2a'
    
    FONT_DEFAULT = '#FFFFFF'
    FONT_DARK = '#262421'
    FONT_ENTRY = '#9E9D9C'
    FONT_RED = '#F27E7E'

class Font_E:
    '''영어 글꼴 상수 클래스'''
    # TODO: 폰트 없을경우 대처
    # (main에서 from tkinter import font 후 available = font.families() 이렇게 받아오고 함수로 직접 판단) 
    # Kristen ITC, Bahnschrift, Cascadia Mono, 
    TITLE = ('Kristen ITC', 100, 'bold')
    TITLE_SMALL = ('Kristen ITC', 50, 'bold')
    VERSION = ('Kristen ITC', 16)
    ENTRY_USERNAME = ('Bahnschrift', 20)
    BUTTON = ('Arial', 20, 'bold')
    BODY_BIG_BOLD = ('Bahnschrift', 30, 'bold')
    BODY_BOLD = ('Cascadia Mono', 20, 'bold')
    BODY = ('Bahnschrift', 20)
    BODY_ITALIC = ('Bahnschrift', 20, 'italic')
    BODY_SMALL = ('Bahnschrift', 16)
    SMALL = ('Arial', 14)
    ACCOUNT = ('Bahnschrift', 13)
    CAPTION = ('Bahnschrift', 12)

class Font_K:
    '''한글 글꼴 상수 클래스'''
    BODY_BIG = ('가비아 사이', 30)
    CAPTION = ('가비아 사이', 12)
    ENTRY = ('가비아 사이', 20)

class Font_J:
    '''일본어 글꼴 상수 클래스'''
    BODY_BIG = ('UD デジタル 教科書体 N', 30)
    CAPTION = ('UD デジタル 教科書体 N', 12)
    ENTRY = ('UD デジタル 教科書体 N', 20)

class Text_D:
    '''앱에서 사용하는 모든 문구를 언어별로 관리'''
    # 최초로그인 or 연속로그인상태 or 오늘이미 완료 문구
    INITIAL_LOGIN = {
        'K': '안녕하세요. 오늘부터 매일 잘부탁드려요!',
        'J': '初めまして。今日から毎日よろしくお願いします！'
    }
    TODAY_DONE = {
        'K': '수고하셨습니다! 내일 다시 봬요.',
        'J': 'お疲れさまでした！明日もまた、よろしくお願いします。'
    }
    STREAK_0 = {
        'K': '어제 바쁘셨나보네요.. 다시 화이팅!',
        'J': '昨日は忙しかったみたいですね。。また、頑張りましょう！'
    }
    STREAK = {
        'K': '일 연속 로그인! 너무 멋져요~',
        'J': '日連続ログイン！すごいです。'
    }
    # BODY문구
    CONFIRM = {
        'K': '결정',
        'J': '決定'
    }
    ALREADY = {
        'K': '이미 아는 단어라면 ',
        'J': '既知の単語なら'
    }
    DICT = {
        'K': '다음 영어 사전: https://dic.daum.net/index.do?dic=eng ',
        'J': 'ロングマン英和辞典: https://www.ldoceonline.com/jp/browse/english-japanese/ '
    }
    # 팁 문구
    TIP_INITIAL_1 = {
        'K': '우선 아래에 있는 사전에 접속해 단어의 뜻을 적어봅시다.',
        'J': 'まずは、英和辞典に接続し、意味を書いてみましょう。'
    }