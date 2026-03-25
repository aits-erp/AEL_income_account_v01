frappe.ui.form.on("Sales Invoice Item", {
    item_code(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (!row.item_code || !frm.doc.company) return;

        frappe.call({
            method: "sales_invoice_account_mapper.api.get_item_income_account",
            args: {
                item_code: row.item_code,
                company: frm.doc.company
            },
            callback: function (r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, "income_account", r.message);
                }
            }
        });
    }
});
