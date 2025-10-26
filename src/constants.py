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
    FONT_USERNAME = '#9E9D9C'
    FONT_GREEN = '#5d9948'
    FONT_RED = '#F27E7E'
    FONT_BLUE = '#0065b2'

class Font_E:
    '''영어 글꼴 상수 클래스'''
    # TODO: 폰트 없을경우 대처
    # (main에서 from tkinter import font 후 available = font.families() 이렇게 받아오고 함수로 직접 판단) 
    # Kristen ITC, Bahnschrift, Cascadia Mono, 
    TITLE = ('Kristen ITC', 110, 'bold')
    TITLE_SMALL = ('Kristen ITC', 50, 'bold')
    VERSION = ('Kristen ITC', 18)
    ENTRY_USERNAME = ('Bahnschrift', 26)
    ENTRY_DELETE = ('Bahnschrift', 22)
    BUTTON = ('Arial', 20, 'bold')
    BODY_PROGRESS = ('Bahnschrift', 35, 'bold')
    BODY_WORD = ('Bahnschrift', 45, 'bold')
    BODY_WORD_A = ('Bahnschrift', 35, 'bold')
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
    ENTRY = ('가비아 사이', 22)
    CAPTION = ('가비아 사이', 14)
    TIP = ('가비아 사이', 12)

class Font_J:
    '''일본어 글꼴 상수 클래스'''
    BODY_BIG = ('UD デジタル 教科書体 N', 30)
    CAPTION = ('UD デジタル 教科書体 N', 12)
    ENTRY = ('UD デジタル 教科書体 N', 22)
    CAPTION = ('UD デジタル 教科書体 N', 14)
    TIP = ('UD デジタル 教科書体 N', 12)

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
    TITLE1 = {
        'K': '오늘의 단어',
        'J': '今日の単語'
    }
    TITLE2 = {
        'K': '개를 정해 봅시다!',
        'J': '個を決めましょう！'
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
    WARNING_O1 = {
        'K': '오늘의 단어 개수가 ',
        'J': '今日の単語の数が'
    }
    WARNING_O2 = {
        'K': '개를 초과했습니다.',
        'J': '個を超過しました。'
    }
    WARNING_A = {
        'K': '오늘의 단어 개수가 채워진 상태에서는 이 조작이 불가능합니다.',
        'J': '今日の単語の数が貯まった状態では、この操作はできません。'
    }
    WARNING_D = {
        'K': '해당 영단어가 이미 존재합니다.',
        'J': 'その英単語は既に存在します。'
    }
    DICT = {
        'K': '다음 영어 사전: https://dic.daum.net/index.do?dic=eng ',
        'J': 'ロングマン英和辞典: https://www.ldoceonline.com/jp/browse/english-japanese/ '
    }

class Tip:
    '''Tip 라벨 랜덤출력 문구 모음'''
    TIP_D1 = {
        'K': 'Tip. 입력칸에 한글입력시 디자인이 깨지는건 죄송합니다... 안 고쳐지네요.',
        'J': 'Tip. 入力欄に日本語入力のとき、デザインが悪いのはごめんなさい。。治せなくて。'
    }
    TIP_D2 = {
        'K': 'Tip. 스피커 버튼을 누르면 발음이 재생됩니다.',
        'J': 'Tip. スピーカーボタンを押すと、発音が流されます。'
    }
    TIP_D3 = {
        'K': 'Tip. 단어장 레벨을 변경하고 싶으면 새로 회원가입을 해야 합니다.',
        'J': 'Tip. 単語帳の難易度を変えたかったら、新しく会員登録をしなければなりません。'
    }
    TIP_D4 = {
        'K': 'Tip. 매일 비슷한 시간대에 하면 더욱 효과가 좋답니다.',
        'J': 'Tip. 毎日だいたい同じ時間に行うと、より効果的です。'
    }
    TIP_D5 = {
        'K': 'Tip. 아는 단어라고 판단되더라도 한번 더 확인합니다.',
        'J': 'Tip. 知っている単語だと思っても、もう一回確認しましょう。'
    }
    TIP_D6 = {
        'K': 'Tip. 오늘의 단어는 신중하게 고릅시다.',
        'J': 'Tip. 今日の単語は慎重に選びましょう。'
    }
    TIP_D7 = {
        'K': 'Tip. 오른쪽에 단어리스트를 누르면 해당단어화면으로 전환됩니다.',
        'J': 'Tip. 右の単語リストを押すと、該当の単語画面に移ります。'
    }
    TIP_T1 = {
        'K': 'Tip. 복습테스트의 채점은 AI가 진행 합니다.',
        'J': 'Tip. 復習テストの採点はAIが行います。'
    }
    TIP_T2 = {
        'K': 'Tip. 복습테스트시 모범답안과 정확히 일치하지 않아도 괜찮습니다.',
        'J': 'Tip. 復習テストのとき、模範解答と正確に一致しなくても大丈夫です。'
    }
    TIP_T3 = {
        'K': 'Tip. 하루에 12개씩만 완벽하게 외워도, 반년이면 약 2200개의 단어를 외운답니다.',
        'J': 'Tip. 一日に12個ずつ完璧に覚えれば、半年で約2200語の単語を暗記できます。'
    }
    TIP_T4 = {
        'K': 'Tip. 외운 단어는 1일, 3일, 7일, 14일, 28일 후에 복습합니다.',
        'J': 'Tip. 覚えた単語は1日3日7日14日28日後に復習を行います。'
    }
    TIP_B1 = {
        'K': 'Tip. 오전 4시에서 5시까지는 RoaD 이용이 불가능 합니다',
        'J': 'Tip. 午前4時から5時の間はRoaDの利用ができません。'
    }
    TIP_B2 = {
        'K': 'Tip. RoaD는 오전 5시를 기준으로 하루가 지났다고 판단합니다.',
        'J': 'Tip. RoaDは午前5時で、日付が変わったと見なされます。'
    }