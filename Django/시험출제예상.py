# @api_view(['GET','POST'])
# def article_list(request):
#     if request.method == 'GET':
#         # DB에서 모든 Article 객체를 가져옵니다.
#         articles = Article.objects.all().order_by('-pk')
#         serializer = ArticleListSerializer(articles, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         # 사용자가 전달한 데이터 받아서 DB에 넣기.
#         serializer = ArticleListSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
        