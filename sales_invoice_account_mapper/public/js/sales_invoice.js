frappe.ui.form.on("Sales Invoice", {
    setup(frm) {
        frm.__income_account_mapping_in_progress = false;
    },

    refresh(frm) {
        map_income_accounts_for_all_rows(frm);
    },

    company(frm) {
        map_income_accounts_for_all_rows(frm);
    }
});

frappe.ui.form.on("Sales Invoice Item", {
    item_code(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!row.item_code || !frm.doc.company) return;

        set_income_account_for_row(frm, cdt, cdn);
    }
});

function map_income_accounts_for_all_rows(frm) {
    if (!frm.doc.company || !frm.doc.items || !frm.doc.items.length) return;
    if (frm.__income_account_mapping_in_progress) return;

    frm.__income_account_mapping_in_progress = true;

    const promises = [];

    (frm.doc.items || []).forEach((row) => {
        if (!row.item_code) return;

        promises.push(
            frappe.call({
                method: "sales_invoice_account_mapper.api.get_item_income_account",
                args: {
                    item_code: row.item_code,
                    company: frm.doc.company
                }
            }).then((r) => {
                if (r.message && row.income_account !== r.message) {
                    return frappe.model.set_value(row.doctype, row.name, "income_account", r.message);
                }
            })
        );
    });

    Promise.all(promises)
        .then(() => frm.refresh_field("items"))
        .finally(() => {
            frm.__income_account_mapping_in_progress = false;
        });
}

function set_income_account_for_row(frm, cdt, cdn) {
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

// frappe.ui.form.on("Sales Invoice Item", {
//     item_code(frm, cdt, cdn) {
//         let row = locals[cdt][cdn];

//         if (!row.item_code || !frm.doc.company) return;

//         frappe.call({
//             method: "sales_invoice_account_mapper.api.get_item_income_account",
//             args: {
//                 item_code: row.item_code,
//                 company: frm.doc.company
//             },
//             callback: function (r) {
//                 if (r.message) {
//                     frappe.model.set_value(cdt, cdn, "income_account", r.message);
//                 }
//             }
//         });
//     }
// });
