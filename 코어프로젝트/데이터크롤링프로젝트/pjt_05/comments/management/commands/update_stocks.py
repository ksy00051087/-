"""
update_stocks : 자동완성용 종목 목록(comments/data/stocks.json)을 새로 받는다

    python manage.py update_stocks

KRX 기업공시채널(KIND)의 '상장법인목록' 다운로드 파일을 받아
회사명 · 종목코드 · 시장구분만 골라 JSON 으로 저장한다.
(댓글 데이터가 아니라 검색창 후보 표시용 목록이므로 미리 저장해 둔다)
"""

import json
import re
import urllib.request
from pathlib import Path

from django.core.management.base import BaseCommand

KIND_URL = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
OUTPUT_PATH = Path(__file__).resolve().parents[2] / 'data' / 'stocks.json'

# KIND 는 코스피를 '유가(증권시장)'로 표기 -> 화면에는 익숙한 이름으로
MARKET_NAMES = {'유가': '코스피'}


class Command(BaseCommand):
    help = 'KRX 상장법인 목록을 받아 자동완성용 stocks.json 을 만든다'

    def handle(self, *args, **options):
        self.stdout.write('[다운로드] KRX 상장법인 목록 요청 중...')
        with urllib.request.urlopen(KIND_URL, timeout=30) as res:
            html = res.read().decode('euc-kr', errors='ignore')

        stocks = []
        # 표의 한 줄(<tr>) 안의 칸(<td>)을 순서대로 꺼냄 : 회사명, 시장구분, 종목코드, ...
        for row in re.findall(r'<tr>(.*?)</tr>', html, re.S):
            cells = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)]
            if len(cells) < 3:
                continue  # 제목 줄(<th>)은 건너뜀
            name, market, code = cells[0], cells[1], cells[2]
            market = MARKET_NAMES.get(market, market)
            stocks.append({'name': name, 'code': code, 'market': market})

        stocks.sort(key=lambda s: s['name'])

        OUTPUT_PATH.parent.mkdir(exist_ok=True)
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(stocks, f, ensure_ascii=False, indent=0)

        self.stdout.write(self.style.SUCCESS(f'[저장] {len(stocks)}개 종목 -> {OUTPUT_PATH}'))
