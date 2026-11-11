from rest_framework import serializers
from .models import Article, Comment
# 우리는 게시글 CRUD 할 거니까
# 직렬화, 역직렬화의 대상도 article


# 게시글 목록용: 댓글 없이 가볍게
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # Database에 쓸 때는 article 검사하지 말고
    # Database에서 읽어올 땐 article 포함해줘라
    class Meta:
        model = Comment
        fields = '__all__'
        # article은 사용자 입력이 아니라 URL의 article_pk로 지정하므로 읽기 전용
        read_only_fields = ('article',)


# 게시글 상세용: 댓글까지 포함
class ArticleSerializer(serializers.ModelSerializer):
    # comment_set이 있긴 있는데 이거 이용해서 댓글 목록 같이 만들어 달라고 작성
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
