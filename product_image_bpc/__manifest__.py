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
    'name': 'Product Image',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'category': 'sales',
    'website': 'http://www.acespritech.com',
    'version': '14.0.1.0.0',
    'summary': '''
                Product Image
            ''',
    'description': '''
                    This module used to add product image field in sale order line, invoice line, purchase_line and stock lines.
                ''',
    'depends': ['base','sale_management', 'purchase', 'product', 'account', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_image_view.xml',
        'report/sale_report_inherited.xml',
        'report/purchase_report_inherited.xml',
        'report/stock_report_inherited.xml',
        'report/invoice_report_inherited.xml',
        # 'report/mrp_report_inherited.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
