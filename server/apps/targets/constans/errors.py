from typing import Final


class TargetErrors:
    BALANCE_IS_NOT_ENOUGH: Final[str] = 'Недостаточно средств на балансе для внесения начальной суммы'
    CANT_CHANGE_AMOUNT: Final[str] = 'Нельзя изменить ожидаемую сумму цели на значение,меньше текущей накопленной суммы'
    THIS_TERM_PASSED: Final[str] = 'Нельзя указать срок, менее пройденного времени'
    NOT_USERS_TARGET: Final[str] = 'У пользователя нет этой цели'
    TARGET_IS_COMPLETE: Final[str] = 'Эта цель уже завершена'
    TARGET_BALANSE_IS_NOT_ENOUGH: Final[str] = 'У этой цели недостаточно накоплений для завершения'
