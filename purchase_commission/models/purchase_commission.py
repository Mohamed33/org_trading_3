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

from odoo import _, api, exceptions, fields, models


class PurchaseCommission(models.Model):
    _name = "purchase.commission"
    _description = "Commission in purchase"

    name = fields.Char("Name", required=True)
    purchase_commission_type = fields.Selection(
        selection=[("fixed", "Fixed percentage"),("fixed amount", "Fixed Amount"),("section", "By sections")],
        string="Type",
        required=True,
        default="fixed",
    )
    purchase_fix_qty = fields.Float(string="Fixed Percentage/Amount")
    purchase_section_ids = fields.One2many(
        string="Sections",
        comodel_name="purchase.commission.section",
        inverse_name="purchase_commission_id",
    )
    purchase_active = fields.Boolean(default=True)
    invoice_state = fields.Selection(
        [("open", "Invoice Based"), ("paid", "Payment Based")],
        string="Invoice Status",
        required=True,
        default="open",
    )
    purchase_amount_base_type = fields.Selection(
        selection=[("gross_amount", "Gross Amount"), ("net_amount", "Net Amount")],
        string="Base",
        required=True,
        default="gross_amount",
    )

    def calculate_section(self, base):
        self.ensure_one()
        for section in self.purchase_section_ids:
            if section.purchase_amount_from <= base <= section.purchase_amount_to:
                return base * section.purchase_percent / 100.0
        return 0.0


class PurchaseCommissionSection(models.Model):
    _name = "purchase.commission.section"
    _description = "Commission section"

    purchase_commission_id = fields.Many2one("purchase.commission", string="Commission")
    purchase_amount_from = fields.Float(string="From")
    purchase_amount_to = fields.Float(string="To")
    purchase_percent = fields.Float(string="Percent", required=True)

    @api.constrains("purchase_amount_from", "purchase_amount_to")
    def _check_amounts(self):
        for section in self:
            if section.purchase_amount_to < section.purchase_amount_from:
                raise exceptions.ValidationError(
                    _("The lower limit cannot be greater than upper one.")
                )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: