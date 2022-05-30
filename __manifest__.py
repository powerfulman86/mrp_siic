# -*- coding: utf-8 -*-
{
    'name': "MRP SIIC Customization",
    'summary': """  MRP SIIC Customization """,
    'description': """ Contacts SIIC Customization  """,
    'author': "SIIC",
    'version': '1.0',
    'category': 'Manufacturing/Manufacturing',
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/mrp_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
