from django.http import JsonResponse
from django.shortcuts import render, redirect
from .crawler import fetch_comments
from .preprocess import CRITERIA, filter_inappropriate, clean_comments
from .augment import augment_comments, merge_with_source
from .summary import summarize_comments
from .suggest import suggest_stocks
from .models import CommentAnalysis

def index(request):
    return render(request, 'comments/index.html')

def suggest(request):
    """검색창 자동완성 : /comments/suggest?q=하 -> 후보 종목 JSON"""
    q = request.GET.get('q', '')
    return JsonResponse({'results': suggest_stocks(q)})

def company(request):
    comname = request.GET.get('comname', '').strip()

    # 입력값이 없으면 아무 동작 없이 입력 화면으로
    if not comname:
        return redirect('comments:index')

    print(comname)  # VS Code 터미널에 회사명 출력
    stock_name, comments = fetch_comments(comname, limit=20)  # comments/crawler.py 의 함수 호출

    # [F611] 예외 상황 안내 : 검색 결과가 없거나, 댓글이 없으면 안내 메시지만 보여줌
    if stock_name is None:
        message = f"'{comname}' 에 대한 검색 결과가 없습니다. 회사명을 다시 확인해 주세요."
    elif not comments:
        message = f"'{stock_name}' 커뮤니티에 수집할 댓글이 없습니다."
    else:
        message = ''

    summary = ''

    if comments:
        kept, removed = filter_inappropriate(comments, CRITERIA['basic'])
        cleaned, iqr_info = clean_comments(kept)
        if cleaned:
            augmented = augment_comments(cleaned)
        else:
            augmented = []

        # [F610] 수집된 전체 댓글(원본) 기준으로 주요 내용 요약
        summary = summarize_comments(stock_name, comments)

        # 수집에 성공했을 때만 각 단계의 결과를 DB 에 저장 (created_at 은 자동)
        CommentAnalysis.objects.create(
            query=comname,
            stock_name=stock_name,
            raw_comments=comments,
            cleaned_comments=cleaned,
            augmented_comments=augmented,
            iqr_threshold=iqr_info,
        )
    else:
        cleaned = [] 
        iqr_info = {}
        augmented = []

    # 정제 댓글 + 증강 댓글 = 최종 결과
    final = cleaned + augmented

    context = {
        'comname': comname,
        'stock_name': stock_name,
        'raw_comments': comments,
        'cleaned_comments': cleaned,
        'augmented_comments': augmented,
        'final_comments': final,
        'message': message,
        'summary': summary,
    }
    return render(request, 'comments/company.html', context)
