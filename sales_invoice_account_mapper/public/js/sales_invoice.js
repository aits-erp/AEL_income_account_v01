frappe.ui.form.on("Sales Invoice", {
    refresh(frm) {
        map_income_account_for_all_rows(frm);
    },

    company(frm) {
        map_income_account_for_all_rows(frm);
    }
});

frappe.ui.form.on("Sales Invoice Item", {
    item_code(frm, cdt, cdn) {
        set_income_account_in_row(frm, cdt, cdn);
    }
});

function map_income_account_for_all_rows(frm) {
    if (!frm.doc.items || !frm.doc.items.length) return;

    frm.doc.items.forEach(row => {
        if (row.item_code) {
            set_income_account_in_row(frm, row.doctype, row.name);
        }
    });
}

function set_income_account_in_row(frm, cdt, cdn) {
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