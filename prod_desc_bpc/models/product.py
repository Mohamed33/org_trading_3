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
from odoo.exceptions import ValidationError


class Product(models.Model):
    _inherit = 'product.product'

    product_item_code = fields.Char(string='Serial Number')
    product_brand = fields.Many2one('product.brand', string='Brand')
    model_number = fields.Many2one('product.model', string='Model')
    product_size = fields.Many2one('product.size', string='Size')
    gender = fields.Many2one('product.gender', string='Gender')
    status = fields.Many2one('product.status', string='Status')
    attachments = fields.Many2one('product.attachments', string='Attachments')
    product_type = fields.Many2one('product.type', string='Product Type',compute='_compute_product_type')
    # gender = fields.Selection([('Male', 'Male'), ('Female', 'Female')], string="Gender")
    # status = fields.Selection([('New', 'New'), ('Used', 'Used')], string="Status")
    # attachments = fields.Selection([('Box and Warranty', 'Box and Warranty'), ('Only Box', 'Only Box'),('No Attachments', 'No Attachments')], string="Attachments")
    manufacturing_year = fields.Char(string="Manufacturing Year")
    product_code = fields.Char(string='Product Code')

    # _sql_constraints = [('product_code_unique', 'unique(product_code)',
    #                                  "There cannot be multiple product with same product code !"),]

    @api.onchange('product_brand')
    def onchange_product_brand(self):
        for rec in self:
            return {'domain': {'model_number': [('brand_id', '=', rec.product_brand.id)]}}

    @api.depends('type')
    def _compute_product_type(self):
        for product in self:
            pro_id = self.env['product.type'].search([('value', '=', product.type)])
            product.write({'product_type': pro_id})

    @api.constrains('product_code')
    def _check_product_code(self):
        record = self.env['product.product'].search([('id','!=',self.id)])
        for product in record:
            if product.product_code:
                if product.product_code == self.product_code:
                    raise ValidationError(
                        'Product code must be unique !!')

    # @api.model
    # def create(self, vals):
    #     vals['product_code'] = self.env['ir.sequence'].next_by_code('product.code')
    #     return super(Product, self).create(vals)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
