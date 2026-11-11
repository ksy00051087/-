from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET','POST'])
def article_list(request):
    if request.method == 'GET':
        # DB에서 모든 Article 객체를 가져옵니다.
        articles = Article.objects.all().order_by('-pk')
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # 사용자가 전달한 데이터 받아서 DB에 넣기.
        serializer = ArticleListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        



@api_view(['GET', 'PUT', 'DELETE','PATCH'])
def article_detail(request, pk):
    # pk에 해당하는 글이 없으면 404 반환
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'GET':
        # pk로 게시글 조회해서 사용자에게 반환
        # 직렬화
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method in ('PUT', 'PATCH'):
        # 사용자가 입력한 데이터를 이용해서 게시글 수정 (partial=True: 일부 필드만 보내도 됨)
        serializer = ArticleSerializer(instance = article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # 수정된 게시글 데이터를 응답으로 돌려줌 (204는 본문이 비어서 아무것도 안 보임)
            return Response(serializer.data)
        
    elif request.method == 'DELETE':
        article.delete()
        return Response({'result' : 'deleted'}, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, comment_pk):
    # comment_pk에 해당하는 댓글이 없으면 404 반환
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        # comment_pk로 댓글 조회해서 사용자에게 반환
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # 사용자가 입력한 데이터를 이용해서 댓글 수정 (partial=True: 일부 필드만 보내도 됨)
        serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
        # 수정이기 때문에 이미 article 정보를 알고 있다
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
@api_view(['GET'])
def comment_list(request):
    # DB에서 모든 Comment 객체를 가져옵니다. (댓글 생성은 comment_create에서)
    comments = Comment.objects.all().order_by('-pk')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def comment_create(request, article_pk):
    # 댓글을 달 게시글 조회 (없으면 404)
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # 사용자가 보낸 content + URL로 받은 article을 함께 저장
        serializer.save(article=article)
        # 응답할 때는 article을 포함해야 한다... 이거 어떻게 해결?? Serializer에 read_only_fields 설정
        return Response(serializer.data, status=status.HTTP_201_CREATED)
