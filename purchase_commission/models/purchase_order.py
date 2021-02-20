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

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends("order_line.purchase_agent_ids.amount")
    def _compute_purchase_commission_total(self):
        for record in self:
            record.purchase_commission_total = sum(record.mapped("order_line.purchase_agent_ids.amount"))

    purchase_commission_total = fields.Float(
        string="Purchase Commissions", compute="_compute_purchase_commission_total", store=True,
    )

    def recompute_lines_agents(self):
        self.mapped("order_line").recompute_agents()


class PurchaseOrderLine(models.Model):
    _inherit = [
        "purchase.order.line",
        "purchase.commission.mixin",
    ]
    _name = "purchase.order.line"

    purchase_agent_ids = fields.One2many(comodel_name="purchase.order.line.agent")

    @api.depends("order_id.partner_id")
    def _compute_purchase_agent_ids(self):
        self.purchase_agent_ids = False  # for resetting previous agents
        for record in self.filtered(lambda x: x.order_id.partner_id):
            if not record.purchase_commission_free:
                record.purchase_agent_ids = record._prepare_agents_vals_partner(
                    record.order_id.partner_id
                )

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        vals["purchase_agent_ids"] = [
            (0, 0, {"purchase_agent_id": x.purchase_agent_id.id, "purchase_commission_id": x.purchase_commission_id.id})
            for x in self.purchase_agent_ids
        ]
        print("\n\n\n\\n==============vals=======",vals)
        return vals


class PurchaseOrderLineAgent(models.Model):
    _inherit = "purchase.commission.line.mixin"
    _name = "purchase.order.line.agent"
    _description = "Agent detail of commission line in order lines"

    purchase_object_id = fields.Many2one(comodel_name="purchase.order.line")
    currency_id = fields.Many2one(related="purchase_object_id.currency_id")

    @api.depends(
        "purchase_object_id.price_subtotal", "purchase_object_id.product_id", "purchase_object_id.product_uom_qty"
    )
    def _compute_amount(self):
        for line in self:
            order_line = line.purchase_object_id
            line.amount = line._get_commission_amount(
                line.purchase_commission_id,
                order_line.price_subtotal,
                order_line.product_id,
                order_line.product_uom_qty,
            )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: