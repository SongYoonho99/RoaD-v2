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
    FONT_GREEN = '#5d9948'
    FONT_RED = '#F27E7E'
    FONT_BLUE = '#0065b2'

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
    CAPTION = ('가비아 사이', 12)

class Font_J:
    '''일본어 글꼴 상수 클래스'''
    BODY_BIG = ('UD デジタル 教科書体 N', 30)
    CAPTION = ('UD デジタル 教科書体 N', 12)
    ENTRY = ('UD デジタル 教科書体 N', 20)
    CAPTION = ('UD デジタル 教科書体 N', 12)

class Text_D:
    '''오늘의 단어 프레임에서 사용하는 문구를 언어별로 관리'''
    # 최초로그인 or 연속로그인상태 or 오늘이미 완료 문구
    INITIAL_LOGIN = {
        'K': '안녕하세요. 오늘부터 잘부탁드려요!',
        'J': '初めまして。今日からよろしくお願いします！'
    }
    TODAY_DONE = {
        'K': '수고하셨습니다! 내일 다시 봬요.',
        'J': 'お疲れさまでした！明日もまた、よろしくお願いします。'
    }
    STREAK_0 = {
        'K': '최근에 바쁘셨나보네요.. 다시 화이팅!',
        'J': '最近忙しかったみたいですね。。また、頑張りましょう！'
    }
    STREAK = {
        'K': '일 연속 로그인! 너무 멋져요~',
        'J': '日連続ログイン！すごいです。'
    }
    TITLE = {
        'K': '오늘 외울 단어를 정해 봅시다!',
        'J': '今日覚える単語を決めましょう！'
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
    WARNING_W = {
        'K': '영단어를 입력해 주세요.',
        'J': '英単語を書いてください。'
    }
    WARNING_M = {
        'K': '뜻을 입력해 주세요.',
        'J': '意味を書いてください。'
    }
    DICT = {
        'K': '다음 영어 사전: https://dic.daum.net/index.do?dic=eng ',
        'J': 'ロングマン英和辞典: https://www.ldoceonline.com/jp/browse/english-japanese/ '
    }

class Tip:
    '''Tip 라벨 랜덤출력 문구 모음'''
    TIP1 = {
        'K': 'Tip. 복습테스트의 채점은 AI가 진행 합니다.',
        'J': 'Tip. 復習テストの採点はAIが行います。'
    }
    TIP2 = {
        'K': 'Tip. 복습테스트시 모범답안과 정확히 일치하지 않아도 괜찮습니다.',
        'J': 'Tip. 復習テストのとき、模範解答と正確に一致しなくても大丈夫です。'
    }
    TIP3 = {
        'K': 'Tip. 오전 4시에서 5시까지는 RoaD 이용이 불가능 합니다',
        'J': 'Tip. 午前4時から5時の間はRoaDの利用ができません。'
    }
    TIP4 = {
        'K': 'Tip. 입력칸에 한글입력시 디자인이 깨지는건 죄송합니다...',
        'J': 'Tip. 入力欄に日本語入力のとき、デザインが悪いのはごめんなさい。。'
    }
    TIP5 = {
        'K': 'Tip. RoaD는 오전 5시를 기준으로 하루가 지났다고 판단합니다.',
        'J': 'Tip. RoaDは午前5時で、日付が変わったと見なされます。'
    }
    TIP6 = {
        'K': 'Tip. 하루에 12개씩만 완벽하게 외워도, 반년이면 약 2200개의 단어를 외운답니다.',
        'J': 'Tip. 一日に12個ずつ完璧に覚えれば、半年で約2200語の単語を暗記できます。'
    }
    TIP7 = {
        'K': 'Tip. 외운 단어는 1일, 3일, 7일, 14일, 28일 후에 복습합니다.',
        'J': 'Tip. 覚えた単語は1日3日7日14日28日後に復習を行います。'
    }
    TIP8 = {
        'K': 'Tip. 스피커 버튼을 누르면 발음이 재생됩니다.',
        'J': 'Tip. スピーカーボタンを押すと、発音が流されます。'
    }