from decimal import Decimal


def create_obj_for_global_total(aggregate_totals: dict) -> dict[str, Decimal]:
    return {'total': aggregate_totals['total_income'] - aggregate_totals['total_expenses']}
