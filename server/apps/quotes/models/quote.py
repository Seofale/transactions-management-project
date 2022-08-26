from django.db import models


class Quote(models.Model):
    text = models.TextField(max_length=256, unique=True)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'

    def __str__(self) -> str:
        return f'({self.pk}) {self.text}'
