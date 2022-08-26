from typing import Final


class TransactionErrors:
    TRANSACTION_INCOME_WITH_CATEGORY: Final[str] = 'Нельзя выбирать категорию для операции дохода'
    TRANSACTION_EXPENSE_WITH_NO_CATEGORY: Final[str] = 'У операции расхода должна быть категория'


class TransactionCategoryErrors:
    ALREADY_EXISTS: Final[str] = 'У пользоваетля уже существует категория с таким названием'
    NOT_USERS_CATEGORY: Final[str] = 'У пользователя нет такой категории'
