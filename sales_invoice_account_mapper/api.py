import frappe

@frappe.whitelist()
def get_item_income_account(item_code, company):
    if not item_code or not company:
        return ""

    item = frappe.get_doc("Item", item_code)

    # 1. Item Default
    for row in item.get("item_defaults") or []:
        if row.company == company and row.income_account:
            return row.income_account

    # 2. Item Group Default
    item_group = item.item_group
    if item_group:
        income_account = frappe.db.get_value(
            "Item Default",
            {"parent": item_group, "company": company},
            "income_account"
        )
        if income_account:
            return income_account

    # 3. Company Default
    return frappe.db.get_value("Company", company, "default_income_account") or ""
