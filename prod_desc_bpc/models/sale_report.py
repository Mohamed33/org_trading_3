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

from odoo import models, fields, api, _

class SaleReport(models.Model):
    _inherit = 'sale.report'

    product_brand = fields.Many2one('product.brand',string='Brand')
    model_number = fields.Many2one('product.model', string='Model Number')
    product_size = fields.Many2one('product.size', string='Size')
    gender = fields.Many2one('product.gender', string='Gender')
    status = fields.Many2one('product.status', string='Status')
    attachments = fields.Many2one('product.attachments', string='Attachments')
    # product_type = fields.Many2one('product.type', string='Product Type')

    # product_id = fields.Many2one('product.product', 'Product Attribute', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['product_brand'] = ', p.product_brand as product_brand'
        fields['model_number'] = ', p.model_number as model_number'
        fields['product_size'] = ', p.product_size as product_size'
        fields['gender'] = ', p.gender as gender'
        fields['status'] = ', p.status as status'
        fields['attachments'] = ', p.attachments as attachments'
        # fields['product_type'] = ', p.product_type as product_type'

        groupby += """, p.product_brand
        , p.model_number
        , p.product_size
        , p.gender
        , p.status
        , p.attachments
        """
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: