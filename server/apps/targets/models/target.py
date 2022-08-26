from decimal import Decimal
from datetime import date

from django.core.validators import MinValueValidator
from django.db import models

from ..add_months import add_months_to_date
from .managers import TargetManager


class Target(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название цели',
    )
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='targets',
        verbose_name='Пользователь',
    )
    category = models.ForeignKey(
        to='pockets.TransactionCategory',
        on_delete=models.CASCADE,
        related_name='targets',
        verbose_name='Категория цели',
        blank=True,
        null=True,
    )
    start_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма начального взноса',
        validators=(MinValueValidator(Decimal('0.00')),),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Общая сумма цели',
        validators=(MinValueValidator(Decimal('0.01')),),
    )
    term = models.IntegerField(
        verbose_name='Срок в месяцах',
        validators=(MinValueValidator(1),),
    )
    start_date = models.DateField(
        verbose_name='Дата создания цели',
        auto_now_add=True,
    )
    percent = models.IntegerField(
        verbose_name='Ставка в процентах',
        validators=(MinValueValidator(1),),
    )
    is_complete = models.BooleanField(default=False)
    complete_date = models.DateField(
        blank=True,
        null=True
    )
    objects = TargetManager()

    @property
    def get_days_to_end(self):
        return (add_months_to_date(self.start_date, self.term) - date.today()).days

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    def __str__(self) -> str:
        return f'{self.user} {self.category}'
