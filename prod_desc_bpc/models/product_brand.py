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


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = "product brand"

    name = fields.Char(string='Brand Name')
    model_ids = fields.One2many('product.model', 'brand_id',
                                  string='Models')

class ProductModel(models.Model):
    _name = 'product.model'
    _description = "product model"

    name = fields.Char(string='Model Name')
    brand_id = fields.Many2one('product.brand', string='Brand')

class ProductSize(models.Model):
    _name = 'product.size'
    _description = "product size"

    name = fields.Char(string='Size')

class ProductForGender(models.Model):
    _name = 'product.gender'

    name = fields.Char("Gender")

class ProductStatus(models.Model):
    _name = 'product.status'

    name = fields.Char("Status")

class ProductAttachments(models.Model):
    _name = 'product.attachments'

    name = fields.Char("Attachments")

class ProductType(models.Model):
    _name = 'product.type'

    name = fields.Char("Type")
    value = fields.Char("Type Value")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: