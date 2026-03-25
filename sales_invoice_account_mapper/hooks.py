app_name = "sales_invoice_account_mapper"
app_title = "Sales Invoice Account Mapper"
app_publisher = "h"
app_description = "hhh"
app_email = "nehalp@11"
app_license = "mit"

# Apps
# ------------------
doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js",
     "Purchase Order": "public/js/purchase_order.js"

}

doc_events = {
    "Sales Invoice": {
        "validate": "sales_invoice_account_mapper.doc_events.set_income_account_on_sales_invoice"
    }
}

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["dt", "=", "Purchase Order Item"],
            ["fieldname", "in", ["custom_custom_rate", "custom_cbm", "custom_custom_total", "custom_so_cbm"]]
        ]
    }
]