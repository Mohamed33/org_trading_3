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
    'name': 'Product Description',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'category': 'sales',
    'website': 'http://www.acespritech.com',
    'version': '14.0.1.0.0',
    'summary': '''
                Product Description
            ''',
    'description': '''
                    This module used to add description fields in sale order line, invoice line, purchase_line and stock lines.
                ''',
    'depends': ['base','sale','sale_management', 'purchase', 'product', 'account', 'stock','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_brand_view.xml',
        'views/sale_order_views.xml',
        'views/account_move_view.xml',
        'views/purchase_view.xml',
        'views/stock_picking_view.xml',
        'views/product_form_view.xml',
        'views/contact_form_view.xml',
        'views/employee_form_view.xml',
        'report/sale_report_inherited.xml',
        'report/purchase_report_inherited.xml',
        'report/stock_report_inherited.xml',
        'report/invoice_report_inherited.xml',
    ],
    # "demo": ["demo/product_data_demo.xml"],
    'installable': True,
    'auto_install': False,
    'application': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
