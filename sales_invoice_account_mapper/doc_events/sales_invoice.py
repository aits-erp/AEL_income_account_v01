import frappe


def get_income_account(item_code, company):
    if not item_code or not company:
        return ""

    # 1. Item master defaults
    item = frappe.get_doc("Item", item_code)

    for row in item.get("item_defaults") or []:
        if row.company == company and row.income_account:
            return row.income_account

    # 2. Item Group defaults
    item_group = item.item_group
    if item_group:
        item_group_doc = frappe.get_doc("Item Group", item_group)
        for row in item_group_doc.get("item_defaults") or []:
            if row.company == company and row.income_account:
                return row.income_account

    # 3. Company default income account
    company_default_income_account = frappe.db.get_value(
        "Company",
        company,
        "default_income_account"
    )
    if company_default_income_account:
        return company_default_income_account

    return ""


def set_income_account_on_sales_invoice(doc, method=None):
    if not doc.company or not doc.items:
        return

    for row in doc.items:
        if not row.item_code:
            continue

        income_account = get_income_account(row.item_code, doc.company)

        if income_account:
            row.income_account = income_account