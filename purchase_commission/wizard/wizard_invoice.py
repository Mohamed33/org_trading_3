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
from odoo import _, fields, models


class PurchaseCommissionMakeInvoice(models.TransientModel):
    _name = "purchase.commission.make.invoice"
    _description = "Wizard for making an invoice from a settlement"

    def _default_journal_id(self):
        return self.env["account.journal"].search([("type", "=", "purchase")])[:1]

    def _default_purchase_settlement_ids(self):
        return self.env.context.get("purchase_settlement_ids", [])

    def _default_from_settlement(self):
        return bool(self.env.context.get("purchase_settlement_ids"))

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        required=True,
        domain="[('type', '=', 'purchase')]",
        default=_default_journal_id,
    )
    company_id = fields.Many2one(
        comodel_name="res.company", related="journal_id.company_id", readonly=True
    )
    product_id = fields.Many2one(
        string="Product for invoicing", comodel_name="product.product", required=True
    )
    purchase_settlement_ids = fields.Many2many(
        comodel_name="purchase.commission.settlement",
        relation="purchase_commission_make_invoice_settlement_rel",
        column1="wizard_id",
        column2="purchase_settlement_id",
        domain="[('state', '=', 'settled'),('purchase_agent_type', '=', 'agent'),"
        "('company_id', '=', company_id)]",
        default=_default_purchase_settlement_ids,
    )
    from_settlement = fields.Boolean(default=_default_from_settlement)
    date = fields.Date(default=fields.Date.context_today)

    def button_create(self):
        self.ensure_one()
        if self.purchase_settlement_ids:
            settlements = self.purchase_settlement_ids
        else:
            settlements = self.env["purchase.commission.settlement"].search(
                [
                    ("state", "=", "settled"),
                    ("purchase_agent_type", "=", "agent"),
                    ("company_id", "=", self.journal_id.company_id.id),
                ]
            )
        print("\n\n\n\n\button create=====",self.journal_id, self.product_id,self.date)
        invoices = settlements.make_invoices(
            self.journal_id, self.product_id, date=self.date
        )
        # go to results
        if len(settlements):
            return {
                "name": _("Created Invoices"),
                "type": "ir.actions.act_window",
                "views": [[False, "list"], [False, "form"]],
                "res_model": "account.move",
                "domain": [["id", "in", invoices.ids]],
            }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: