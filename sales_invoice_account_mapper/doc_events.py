import frappe
from sales_invoice_account_mapper.api import get_item_income_account


def set_income_account_on_sales_invoice(doc, method=None):
    if not doc.company or not doc.items:
        return

    for row in doc.items:
        if row.item_code and not row.income_account:
            income_account = get_item_income_account(row.item_code, doc.company)
            if income_account:
                row.income_account = income_account