app_name = "sales_invoice_account_mapper"
app_title = "Sales Invoice Account Mapper"
app_publisher = "h"
app_description = "hhh"
app_email = "nehalp@11"
app_license = "mit"

# Apps
# ------------------
doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js"
}

doc_events = {
    "Sales Invoice": {
        "validate": "sales_invoice_account_mapper.doc_events.set_income_account_on_sales_invoice"
    }
}