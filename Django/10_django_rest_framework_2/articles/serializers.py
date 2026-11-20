from os import read

from rest_framework import serializers

from .models import Article, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "content",
        )


class ArticleSerializer(serializers.ModelSerializer):
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = (
                "id",
                "content",
            )

    num_of_comments = serializers.SerializerMethodField()
    comment_set = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = "__all__"

    def get_num_of_comments(self, obj):
        if hasattr(obj, "num_of_comments"):
            return obj.num_of_comments
        return obj.comment_set.count()


class CommentSerializer(serializers.ModelSerializer):
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ("title",)

    article = ArticleTitleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
