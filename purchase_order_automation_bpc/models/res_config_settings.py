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

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # is_delivery_set_to_done = fields.Boolean(string="Is Delivery Set to Done")
    # create_invoice = fields.Boolean(string='Create Invoice?')
    # validate_invoice = fields.Boolean(string='Validate invoice?')

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            is_delivery_set_to_done_purchase=bool(params.get_param('is_delivery_set_to_done_purchase')),
            create_invoice_purchase=bool(params.get_param('create_invoice_purchase')),
            validate_invoice_purchase=bool(params.get_param('validate_invoice_purchase'))
        )
        return res

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('is_delivery_set_to_done_purchase', self.is_delivery_set_to_done_purchase)
        params.set_param('create_invoice_purchase', self.create_invoice_purchase)
        params.set_param('validate_invoice_purchase', self.validate_invoice_purchase)

    is_delivery_set_to_done_purchase = fields.Boolean(string="Is Delivery Set to Done")
    create_invoice_purchase = fields.Boolean(string='Create Invoice?')
    validate_invoice_purchase = fields.Boolean(string='Validate invoice?')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: