"""
summary.py : 댓글 요약 모듈 (심화 F610)

    from .summary import summarize_comments
    summary = summarize_comments('삼성전자', comments)
"""

from .llm import run_llm


def build_summary_prompt(stock_name, comments):
    """수집된 댓글 전체를 주고, 주요 내용을 요약해 달라는 프롬프트를 만든다"""
    numbered = '\n'.join(f'{i}. {c}' for i, c in enumerate(comments))
    return f"""다음은 토스증권 '{stock_name}' 종목 커뮤니티에 올라온 댓글 {len(comments)}개야.
댓글 전체의 주요 내용을 한국어로 요약해줘.
- 3~5개 문장으로, 각 문장은 줄바꿈으로 구분
- 투자자들의 전반적인 분위기(긍정/부정/중립)를 첫 문장에 적기
- 자주 언급되는 주제(주가, 실적, 매수·매도 의견 등)를 정리하기
- 욕설이나 비방은 옮기지 말고, 마크다운·번호·코드블럭은 쓰지 마

댓글 목록:
{numbered}"""


def summarize_comments(stock_name, comments):
    """LLM 으로 댓글을 요약한 문자열을 돌려준다 (댓글이 없거나 실패하면 빈 문자열)"""
    if not comments:
        return ''

    print(f'[요약] LLM 호출 중... (댓글 {len(comments)}개)')
    try:
        return run_llm(build_summary_prompt(stock_name, comments)).strip()
    except Exception as e:
        # 요약은 부가 기능이라, 실패해도 나머지 결과 화면은 그대로 보여줌
        print('[요약 실패]', e)
        return ''
