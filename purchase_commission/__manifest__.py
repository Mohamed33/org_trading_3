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
    "name": "Purchase commissions",
    "version": "14.0.1.0.0",
    "author": "Acespritech Solutions Pvt. Ltd.",
    "category": "Purchase",
    "depends": ["account", "product", "sale_management","purchase",'sale_purchase'],
    "website": "http://www.acespritech.com",
    "data": [
        "security/ir.model.access.csv",
        "security/purchase_commission_security.xml",
        "views/purchase_commission_view.xml",
        "views/purchase_commission_mixin_views.xml",
        "views/product_template_view.xml",
        "views/res_partner_view.xml",
        "views/purchase_order_view.xml",
        "views/account_move_views.xml",
        "views/purchase_commission_settlement_view.xml",
        "views/purchase_commission_settlement_report.xml",
        "views/report_settlement_templates.xml",
        "report/purchase_commission_analysis_report_view.xml",
        "wizard/wizard_settle.xml",
        "wizard/wizard_invoice.xml",
    ],
    "demo": ["demo/purchase_agent_demo.xml"],
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: