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


class Partner(models.Model):
    _inherit = 'res.partner'

    contact_code = fields.Char(string='Contact Code')

    @api.constrains('contact_code')
    def _check_contact_code(self):
        record = self.env['res.partner'].search([('id', '!=', self.id)])
        for partner in record:
            if partner.contact_code:
                if partner.contact_code == self.contact_code:
                    raise ValidationError(
                        'Contact code must be unique !!')

    # @api.model
    # def create(self, vals):
    #     vals['contact_code'] = self.env['ir.sequence'].next_by_code('contact.code')
    #     return super(Partner, self).create(vals)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: