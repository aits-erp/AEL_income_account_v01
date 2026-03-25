import frappe
from frappe.utils import flt


@frappe.whitelist()
def calculate_po_item_values(custom_rate=0, cbm=0, so_cbm=0):
    custom_rate = flt(custom_rate)
    cbm = flt(cbm)
    so_cbm = flt(so_cbm)

    custom_total = 0
    final_rate = 0

    if cbm > 0:
        custom_total = custom_rate / cbm
        final_rate = custom_total * so_cbm

    return {
        "custom_total": custom_total,
        "rate": final_rate
    }