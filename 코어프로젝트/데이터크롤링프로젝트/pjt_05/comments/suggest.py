"""
suggest.py : 검색창 자동완성 후보 모듈

    from .suggest import suggest_stocks
    suggest_stocks('하')  # -> [{'name': '하나금융지주', 'code': '086790', 'market': '코스피'}, ...]

종목 목록은 comments/data/stocks.json (python manage.py update_stocks 로 생성)
"""

import json
from functools import lru_cache
from pathlib import Path

STOCKS_PATH = Path(__file__).resolve().parent / 'data' / 'stocks.json'


@lru_cache(maxsize=1)
def load_stocks():
    """종목 목록 파일을 읽는다 (처음 한 번만 읽고 이후에는 메모리에 둔 값을 재사용)"""
    if not STOCKS_PATH.exists():
        print('[자동완성] stocks.json 이 없습니다. python manage.py update_stocks 를 실행하세요.')
        return []
    with open(STOCKS_PATH, encoding='utf-8') as f:
        return json.load(f)


def suggest_stocks(query, limit=10):
    """query 가 이름(또는 종목코드)에 들어간 종목을 최대 limit 개 돌려준다"""
    q = query.strip().lower()
    if not q:
        return []

    matches = []
    for stock in load_stocks():
        name = stock['name'].lower()
        if name.startswith(q):
            rank = 0  # 이름이 입력값으로 "시작"하면 가장 먼저
        elif q in name:
            rank = 1  # 이름 "중간"에 들어 있으면 그다음
        elif stock['code'].startswith(q):
            rank = 2  # 종목코드로 검색한 경우
        else:
            continue
        # 같은 순위라면 코스피 종목 -> 이름이 짧은 것(= 입력값과 더 가까운 것) 순으로
        is_not_kospi = stock['market'] != '코스피'
        matches.append((rank, is_not_kospi, len(stock['name']), stock['name'], stock))

    matches.sort(key=lambda m: m[:4])
    return [m[4] for m in matches[:limit]]
