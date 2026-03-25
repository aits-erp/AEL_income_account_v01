frappe.ui.form.on("Purchase Order Item", {
	custom_custom_rate(frm, cdt, cdn) {
		call_po_calculation(cdt, cdn);
	},
	custom_cbm(frm, cdt, cdn) {
		call_po_calculation(cdt, cdn);
	},
	custom_so_cbm(frm, cdt, cdn) {
		call_po_calculation(cdt, cdn);
	}
});

function call_po_calculation(cdt, cdn) {
	let row = locals[cdt][cdn];

	frappe.call({
		method: "sales_invoice_account_mapper.api.calculate_po_item_values",
		args: {
			custom_custom_rate: row.custom_custom_rate || 0,
			custom_cbm: row.custom_cbm || 0,
			custom_so_cbm: row.custom_so_cbm || 0
		},
		callback: function(r) {
			if (r.message) {
				frappe.model.set_value(cdt, cdn, "custom_custom_total", r.message.custom_custom_total || 0);
				frappe.model.set_value(cdt, cdn, "rate", r.message.rate || 0);
			}
		}
	});
}