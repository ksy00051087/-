# 문제 10. [서술형] 1:N 관계의 읽기 전용 필드

댓글 생성 시 `CommentSerializer` 의 `article` 필드를 읽기 전용(`read_only`)으로 지정하는 이유를 설명하고, 이 때 `views.py` 에서 `serializer.save(article=article)` 처럼 게시글을 따로 전달해야 하는 이유를 설명하시오.

## 답안

