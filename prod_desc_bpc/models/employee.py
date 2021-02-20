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


class Employee(models.Model):
    _inherit = 'hr.employee'

    emp_code = fields.Char(string='Employee Code')

    @api.constrains('emp_code')
    def _check_emp_code(self):
        record = self.env['hr.employee'].search([('id', '!=', self.id)])
        for employee in record:
            if employee.emp_code:
                if employee.emp_code == self.emp_code:
                    raise ValidationError(
                        'Employee code must be unique !!')

    # @api.model
    # def create(self, vals):
    #     vals['emp_code'] = self.env['ir.sequence'].next_by_code('emp.code')
    #     return super(Employee, self).create(vals)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: