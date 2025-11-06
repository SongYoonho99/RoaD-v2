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
    MANUAL_K = os.path.join(BASE_DIR, 'manual_k.png')
    MANUAL_J = os.path.join(BASE_DIR, 'manual_j.png')
    MANUAL_ADD_K = os.path.join(BASE_DIR, 'manual_add_k.png')
    MANUAL_ADD_J = os.path.join(BASE_DIR, 'manual_add_j.png')
    SQUARE_PROGRESS = os.path.join(BASE_DIR, 'square_progress.png')
    SQUARE_MEAN_K = os.path.join(BASE_DIR, 'square_mean_k.png')
    SQUARE_DICT_K = os.path.join(BASE_DIR, 'square_dict_k.png')
    SQUARE_MEAN_J = os.path.join(BASE_DIR, 'square_mean_j.png')
    SQUARE_DICT_J = os.path.join(BASE_DIR, 'square_dict_j.png')
    SQUARE_KNOW_K = os.path.join(BASE_DIR, 'square_know_k.png')
    SQUARE_KNOW_J = os.path.join(BASE_DIR, 'square_know_j.png')
    SQUARE_RIGHT_K = os.path.join(BASE_DIR, 'square_right_k.png')
    SQUARE_RIGHT_J = os.path.join(BASE_DIR, 'square_right_j.png')
    SQUARE_WORD = os.path.join(BASE_DIR, 'square_word.png')
    SQUARE_MEAN_ADD_K = os.path.join(BASE_DIR, 'square_mean_add_k.png')
    SQUARE_MEAN_ADD_J = os.path.join(BASE_DIR, 'square_mean_add_j.png')
    SQUARE_RIGHT_ADD = os.path.join(BASE_DIR, 'square_right_add.png')

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
    CONFIRM_BUTTON = ('가비아 사이', 22)
    BODY = ('가비아 사이', 20)
    BODY_SMALL = ('가비아 사이', 18)
    ENTRY_CONFIRM = ('가비아 사이', 18)
    CAPTION = ('가비아 사이', 14)
    CAPTION_SMALL = ('가비아 사이', 12)
    MODIFY_BUTTON = ('가비아 사이', 12)
    TIP = ('가비아 사이', 12)

class Font_J:
    '''일본어 글꼴 상수 클래스'''
    BODY_BIG = ('UD デジタル 教科書体 N', 30)
    CAPTION = ('UD デジタル 教科書体 N', 12)
    ENTRY = ('UD デジタル 教科書体 N', 22)
    CONFIRM_BUTTON = ('UD デジタル 教科書体 N', 22)
    BODY = ('UD デジタル 教科書体 N', 20)
    BODY_SMALL = ('UD デジタル 教科書体 N', 18)
    ENTRY_CONFIRM = ('UD デジタル 教科書体 N', 18)
    CAPTION = ('UD デジタル 教科書体 N', 14)
    CAPTION_SMALL = ('UD デジタル 教科書体 N', 12)
    MODIFY_BUTTON = ('UD デジタル 教科書体 N', 12)
    TIP = ('UD デジタル 教科書体 N', 12)

class Text_D:
    '''오늘의 단어 프레임에서 사용하는 문구를 언어별로 관리'''
    # 매뉴얼 문구
    MANUAL_TITLE = {
        'K': '단어 등록 메뉴얼',
        'J': '単語登録マニュアル'
    }
    MANUAL_1 = {
        'K': '이 단계는 테스트가 아닌 오늘의 단어를 등록하는 단계입니다.',
        'J': 'このステップはテストではなく、今日の単語を登録するステップです。'
    }
    MANUAL_2 = {
        'K': '이 부분은 목표한 단어수까지 얼마나 단어를 채웠는지를 나타냅니다.',
        'J': 'この部分は目標した単語数まで、あと何個残っているかを示しています。'
    }
    MANUAL_3 = {
        'K': '아래 사전을 참고하여 앞으로 외울 단어의 뜻을 자유롭게 적어주시면 됩니다.',
        'J': '下の辞典を参考にし、これから覚える単語の意味を自由に書いてください。'
    }
    MANUAL_ADD_3 = {
        'K': '외우고 싶은 영단어와 그 뜻을 각각의 빈칸에 자유롭게 적어주시면 됩니다.',
        'J': '覚えたい英単語とその意味を各々の欄に自由に書いて下さい。'
    }
    MANUAL_4 = {
        'K': '이미 아는 단어라, 외울 필요가 없다면 이 부분을 눌러주세요.',
        'J': 'すでに既知の単語で、覚える必要がないのであれば、ここを押してください。'
    }
    MANUAL_ADD_4 = {
        'K': '초록색이 추가된 단어이며, 이곳을 직접 클릭하여 편집도 가능합니다.',
        'J': '緑が追加された単語で、直接クリックして編集もできます。'
    }
    MANUAL_5 = {
        'K': '초록색이 외울단어, 파란색이 이미 아는 단어이며, 클릭하여 편집도 가능합니다.',
        'J': '緑が覚える単語、青が既知の単語で、クリックして編集もできます。'
    }
    NEXT = {
        'K': '다음',
        'J': '次へ'
    }
    START = {
        'K': '시작',
        'J': 'スタート'
    }

    # 최초로그인 or 연속로그인상태 or 오늘이미 완료 문구
    INITIAL_LOGIN = {
        'K': '안녕하세요. 오늘부터 잘부탁드려요!',
        'J': '初めまして。今日からよろしくお願いします！'
    }
    DONE_TODAY = {
        'K': '수고하셨습니다! 내일 다시 봬요.',
        'J': 'お疲れさまでした！明日もまた、よろしくお願いします。'
    }
    STREAK_P = {
        'K': '일 연속 로그인!!',
        'J': '日連続ログイン！！'
    }
    STREAK_N = {
        'K': '일간 바쁘셨나보네요.. 다시 열심히 해봐요!',
        'J': '日間忙しかったようですね。。また、頑張りましょう！'
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
    TITLE_CONFIRM_WORD_WINDOW = {
        'K': '외울 단어 최종 확인',
        'J': '覚える単語最終確認'
    }
    MODYFICATION = {
        'K': '수정',
        'J': '修正'
    }
    START_TEST = {
        'K': '결정 후 복습테스트 시작',
        'J': '決定して復習テストスタート'
    }
    WARNING_C = {
        'K': '모든 단어의 수정작업을 마치고 테스트를 진행 해주세요.',
        'J': 'すべての単語の修正を終えてからテストを行ってください。'
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
        'K': 'Tip. 이거 수정해',
        'J': 'Tip. 午前4時から5時の間はRoaDの利用ができません。'
    }
    TIP_B2 = {
        'K': 'Tip. RoaD는 오전 5시를 기준으로 하루가 지났다고 판단합니다.',
        'J': 'Tip. RoaDは午前5時で、日付が変わったと見なされます。'
    }