from django.db import models

class CommentAnalysis(models.Model):
    query = models.CharField(max_length=50)
    stock_name = models.CharField(max_length=50)
    raw_comments = models.JSONField(default=list)
    cleaned_comments = models.JSONField(default=list)
    augmented_comments = models.JSONField(default=list)
    iqr_threshold = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.stock_name} ({self.created_at:%Y-%m-%d %H:%M})'
