import frappe
from frappe.utils import flt


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
    if item.item_group:
        income_account = frappe.db.get_value(
            "Item Default",
            {
                "parent": item.item_group,
                "company": company,
                "parenttype": "Item Group",
            },
            "income_account",
        )
        if income_account:
            return income_account

    # 3. Company Default
    return frappe.db.get_value("Company", company, "default_income_account") or ""


@frappe.whitelist()
def calculate_po_item_values(custom_custom_rate=0, custom_cbm=0, custom_so_cbm=0):
    custom_custom_rate = flt(custom_custom_rate)
    custom_cbm = flt(custom_cbm)
    custom_so_cbm = flt(custom_so_cbm)

    custom_custom_total = 0
    final_rate = 0

    if custom_cbm > 0:
        custom_custom_total = custom_custom_rate / custom_cbm
        final_rate = custom_custom_total * custom_so_cbm

    return {
        "custom_custom_total": custom_custom_total,
        "rate": final_rate,
    }


# import frappe
# from frappe.utils import flt


# @frappe.whitelist()
# def get_item_income_account(item_code, company):
#     if not item_code or not company:
#         return ""

#     item = frappe.get_doc("Item", item_code)

#     # 1. Item Default
#     for row in item.get("item_defaults") or []:
#         if row.company == company and row.income_account:
#             return row.income_account

#     # 2. Item Group Default
#     item_group = item.item_group
#     if item_group:
#         income_account = frappe.db.get_value(
#             "Item Default",
#             {"parent": item_group, "company": company},
#             "income_account"
#         )
#         if income_account:
#             return income_account

#     # 3. Company Default
#     return frappe.db.get_value("Company", company, "default_income_account") or ""


# @frappe.whitelist()
# def calculate_po_item_values(custom_custom_rate=0, custom_cbm=0, custom_so_cbm=0):
#     custom_custom_rate = flt(custom_custom_rate)
#     custom_cbm = flt(custom_cbm)
#     custom_so_cbm = flt(custom_so_cbm)

#     custom_custom_total = 0
#     final_rate = 0

#     if custom_cbm > 0:
#         custom_custom_total = custom_custom_rate / custom_cbm
#         final_rate = custom_custom_total * custom_so_cbm

#     return {
#         "custom_custom_total": custom_custom_total,
#         "rate": final_rate
#     }