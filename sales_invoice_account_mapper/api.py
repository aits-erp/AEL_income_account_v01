import frappe


@frappe.whitelist()
def get_item_income_account(item_code, company):
    if not item_code or not company:
        return ""

    item = frappe.get_doc("Item", item_code)

    # 1. Check item defaults for matching company
    for row in item.get("item_defaults") or []:
        if row.company == company and row.income_account:
            return row.income_account

    # 2. Optional fallback: Item Group default
    item_group = frappe.db.get_value("Item", item_code, "item_group")
    if item_group:
        income_account = frappe.db.get_value(
            "Item Default",
            {"parent": item_group, "company": company},
            "income_account"
        )
        if income_account:
            return income_account

    # 3. Optional fallback: Company default income account
    company_default_income_account = frappe.db.get_value(
        "Company",
        company,
        "default_income_account"
    )
    if company_default_income_account:
        return company_default_income_account

    return ""