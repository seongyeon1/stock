from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    link = models.URLField(default=None)
    released_date = models.DateField(auto_now_add=True, verbose_name='등록시간')
    ticker = models.ForeignKey('ticker.Ticker', on_delete=models.CASCADE, default=None, verbose_name='종목명')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '뉴스'
        verbose_name_plural = '뉴스'