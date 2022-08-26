from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from .managers import TargetUpdateManager


class TargetUpdate(models.Model):
    target = models.ForeignKey(
        to='targets.Target',
        on_delete=models.CASCADE,
        related_name='updates',
        verbose_name='Цель'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма обновления цели',
        validators=(MinValueValidator(Decimal('0.01')),),
    )
    created_date = models.DateField(
        verbose_name='Дата обновления суммы цели',
        auto_now_add=True,
    )
    is_percent = models.BooleanField(default=False)
    objects = TargetUpdateManager()

    class Meta:
        verbose_name = 'Обновление баланса цели'
        verbose_name_plural = 'Обновляния баланса цели'

    def __str__(self) -> str:
        return f'{self.target}'
