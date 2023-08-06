# Copyright 2021-Coopdevs Treball SCCL (<https://coopdevs.org>)
# - César López Ramírez - <cesar.lopez@coopdevs.org>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "BI View Report",
    "version": "12.0.1.0.0",
    "depends": [
        "bi_view_editor", "mail",
        "report_async"
    ],
    "author": "Coopdevs Treball SCCL",
    "category": "Reporting",
    "website": "https://coopdevs.org",
    "license": "AGPL-3",
    "summary": """
        Create periodic report sended by email using bi_view_editor
    """,
    "data": [
        'reports/bi_view_report_email_template.xml',
        'wizards/bi_view_report_wizard.xml',
    ],
    "installable": True,
}
