'''텍스트파일로 되어있는 영단어 데이터를 데이터베이스 단어목록에 추가'''
import os
import re

import requests
from dotenv import load_dotenv

table_name = ''  # 생성할 테이블 이름('word_'로 시작해야 하고 20자 이내여야 함)
txt_file_name = ''  # 읽어올 텍스트 파일 이름

# EC2 인스턴스 서버의 기본 주소
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
EC2_IP = os.getenv('EC2_IP')
base_URL = f'http://{EC2_IP}:5000/'  # 베이스 URL

def read_txt():
    '''텍스트파일 읽고 words 리스트에 격납'''
    words = []
    try:
        with open(txt_file_name, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, start=1):
                word = line.strip()
                if not word:
                    continue
                if not re.fullmatch(r'[A-Za-z ]+', word) or len(word) > 20:
                    print(f'{i}행 "{word}" 오류')
                    return None
                words.append(word)
        print(f'{len(words)}개의 단어 읽기 성공')
        return words

    except FileNotFoundError:
        print(f'"{txt_file_name}"을(를) 찾을 수 없습니다.')
        return None
    except Exception as e:
        print(f'파일 읽기 중 오류 발생: {e}')
        return None

def txt_to_db(words):
    '''서버로 데이터 전송'''
    payload = {'table_name': table_name, 'words': words}
    try:
        URL = f'{base_URL}create_word_category'
        response = requests.post(URL, json=payload)
        if response.status_code == 200:
            print('새로운 단어 카테고리 테이블 생성 및 단어 삽입 성공')
        else:
            print(response.json().get('message'))
    except Exception as e:
        print(f'서버 연결 실패: {e}')
        return

if __name__ == '__main__':
    words = read_txt()
    if words:
        txt_to_db(words)