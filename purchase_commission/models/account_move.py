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


class AccountMove(models.Model):
    _inherit = "account.move"

    purchase_commission_total = fields.Float(
        string="Purchase Commissions", compute="_compute_purchase_commission_total", store=True,
    )
    purchase_settlement_id = fields.Many2one(
        comodel_name="purchase.commission.settlement",
        help="Settlement that generates this invoice",
        copy=False,
    )

    @api.depends("line_ids.purchase_agent_ids.amount")
    def _compute_purchase_commission_total(self):
        for record in self:
            record.purchase_commission_total = 0.0
            for line in record.line_ids:
                record.purchase_commission_total += sum(x.amount for x in line.purchase_agent_ids)

    def button_cancel(self):
        """Put settlements associated to the invoices in exception."""
        self.purchase_settlement_id.state = "except_invoice"
        return super().button_cancel()

    def post(self):
        """Put settlements associated to the invoices in invoiced state."""
        self.purchase_settlement_id.state = "invoiced"
        return super().post()

    def recompute_lines_agents(self):
        self.mapped("invoice_line_ids").recompute_agents()


class AccountMoveLine(models.Model):
    _inherit = [
        "account.move.line",
        "purchase.commission.mixin",
    ]
    _name = "account.move.line"

    purchase_agent_ids = fields.One2many(comodel_name="purchase.account.invoice.line.agent")
    any_settled = fields.Boolean(compute="_compute_any_settled")

    @api.depends("purchase_agent_ids", "purchase_agent_ids.settled")
    def _compute_any_settled(self):
        for record in self:
            record.any_settled = any(record.mapped("purchase_agent_ids.settled"))

    @api.depends("move_id.partner_id")
    def _compute_purchase_agent_ids(self):
        self.purchase_agent_ids = False  # for resetting previous agents
        for record in self.filtered(
                lambda x: x.move_id.partner_id and x.move_id.move_type == "in_invoice"
        ):
            if not record.purchase_commission_free and record.product_id:
                record.purchase_agent_ids = record._prepare_agents_vals_partner(
                    record.move_id.partner_id
                )


class AccountInvoiceLineAgent(models.Model):
    _inherit = "purchase.commission.line.mixin"
    _name = "purchase.account.invoice.line.agent"
    _description = "Agent detail of commission line in invoice lines"

    purchase_object_id = fields.Many2one(comodel_name="account.move.line")
    purchase_invoice_id = fields.Many2one(
        string="Invoice",
        comodel_name="account.move",
        related="purchase_object_id.move_id",
        store=True,
    )
    invoice_date = fields.Date(
        string="Invoice date", related="purchase_invoice_id.date", store=True, readonly=True,
    )
    purchase_agent_line = fields.Many2many(
        comodel_name="purchase.commission.settlement.line",
        relation="purchase_settlement_agent_line_rel",
        column1="purchase_agent_line_id",
        column2="purchase_settlement_id",
        copy=False,
    )
    settled = fields.Boolean(compute="_compute_settled", store=True)
    company_id = fields.Many2one(
        comodel_name="res.company", compute="_compute_company", store=True,
    )
    currency_id = fields.Many2one(related="purchase_object_id.currency_id", readonly=True,)

    @api.depends("purchase_object_id.price_subtotal", "purchase_object_id.product_id.purchase_commission_free")
    def _compute_amount(self):
        for line in self:
            inv_line = line.purchase_object_id
            line.amount = line._get_commission_amount(
                line.purchase_commission_id,
                inv_line.price_subtotal,
                inv_line.product_id,
                inv_line.quantity,
            )
            # Refunds commissions are negative
            if line.purchase_invoice_id.move_type and "refund" in line.purchase_invoice_id.move_type:
                line.amount = -line.amount

    @api.depends(
        "purchase_agent_line", "purchase_agent_line.purchase_settlement_id.state", "purchase_invoice_id", "purchase_invoice_id.state"
    )
    def _compute_settled(self):
        # Count lines of not open or paid invoices as settled for not
        # being included in settlements
        for line in self:
            line.settled = any(
                x.purchase_settlement_id.state != "cancel" for x in line.purchase_agent_line
            )

    @api.depends("purchase_object_id", "purchase_object_id.company_id")
    def _compute_company(self):
        for line in self:
            line.company_id = line.purchase_object_id.company_id

    @api.constrains("purchase_agent_id", "amount")
    def _check_settle_integrity(self):
        for record in self:
            if any(record.mapped("settled")):
                raise exceptions.ValidationError(_("You can't modify a settled line"),)

    def _skip_settlement(self):
        """This function should return if the commission can be payed.

        :return: bool
        """
        self.ensure_one()
        return (
            self.purchase_commission_id.invoice_state == "paid"
            and self.purchase_invoice_id.invoice_payment_state != "paid"
        ) or self.purchase_invoice_id.state != "posted"

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: