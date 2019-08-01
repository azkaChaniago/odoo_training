# -*- coding: utf-8 -*-
{
    'name': "Default Experienced",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Some purpose here
        module path => ~/.local/share/Odoo/addons/10.0/exp_default
    """,

    'author': "Azka Chaniago",
    'website': "http://127.0.0.1:8070",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'report'],

    # always loaded
    'data': [
        'report/report_view.xml',
        'wizard/wizard_view.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/partner.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}