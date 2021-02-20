# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': " Purchase Order Automation",
    'version': "14.0.0.1",
    'sequence': 1,
    "author": "Acespritech Solutions Pvt. Ltd.",
    "website": "http://www.acespritech.com",
	'support': 'odoo.support@wedotech-s.com',
    'license': 'OPL-1',
    'category': "purchase",
     'summary': """
    Automatic Generate Invoice and Picking when purchase order confirm.
    """,
    'description': """
    Automatic Generate Invoice and Picking when purchase order confirm.
    """, 
    'depends': ['purchase'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
