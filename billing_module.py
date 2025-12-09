def log_expense(item_name, cost, quantity_used):
    """
    Mock function to log expense to accounting/billing.
    """
    print(f"[BILLING] Charged {cost} for {quantity_used}x {item_name}")
    return True
