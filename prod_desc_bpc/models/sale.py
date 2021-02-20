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

from odoo import models, fields, api


class Sale(models.Model):
    _inherit = 'sale.order'

    product_item_code = fields.Char(related="order_line.product_item_code", string='Serial Number')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_item_code = fields.Char(string='Serial Number')
    product_brand = fields.Many2one('product.brand', string='Brand')
    model_number = fields.Many2one('product.model', string='Model Number')
    product_size = fields.Many2one('product.size', string='Size')
    attachments = fields.Many2one('product.attachments', string='Attachments')
    status = fields.Many2one('product.status', string='Status')
    gender = fields.Many2one('product.gender', string='Gender')
    manufacturing_year = fields.Char(string='Year')
    

    @api.onchange('product_brand')
    def onchange_product_brand(self):
        for rec in self:
            return {'domain': {'model_number': [('brand_id', '=', rec.product_brand.id)]}}

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        self.product_item_code = self.product_id.product_item_code
        self.product_brand = self.product_id.product_brand
        self.model_number = self.product_id.model_number
        self.product_size = self.product_id.product_size
        self.attachments = self.product_id.attachments
        self.status = self.product_id.status
        self.gender = self.product_id.gender
        self.manufacturing_year = self.product_id.manufacturing_year
        return res

    def create(self, vals):
        if isinstance(vals, list):
            for rec in vals:
                product_id = self.env['product.product'].browse(rec.get('product_id'))
                rec.update({'product_item_code': product_id.product_item_code,
                            'product_brand': product_id.product_brand.id,
                            'model_number': product_id.model_number.id})
        res = super(SaleOrderLine, self).create(vals)
        return res

    @api.onchange('product_item_code')
    def _onchange_product_item_code(self):
        if self.product_item_code:
            pro_id = self.env['product.product'].search([('product_item_code', '=', self.product_item_code)], limit=1)
            self.write({'product_id': pro_id})

    @api.onchange('model_number')
    def _onchange_model_number(self):
        if self.model_number:
            pro_id = self.env['product.product'].search([('model_number', '=', self.model_number.id)], limit=1)
            self.write({'product_id': pro_id})


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
