{
    'name': "Odoo Biba Ardoak customizations",
    'version': '14.0.0.0.2',
    'depends': ['base', 'sale_stock'],
    'author': "Coopdevs Treball SCCL",
    'website': 'https://coopdevs.org',
    'category': "Cooperative management",
    'description': """
    Odoo Biba Ardoak customizations.
    """,
    "license": "AGPL-3",
    'data': [
        "data/ir_config_parameter.xml",
        "report/delivery_note_mail_template.xml",
        "report/report_picking_batch_delivery_note.xml",
        "report/stock_picking_batch_report_views.xml",
        "security/ir.model.access.csv",
        "views/report_view.xml",
        "wizards/send_delivery_note/send_delivery_note.xml"
    ],
}
