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

from odoo import _, api, fields, models


class PurchaseCommissionMixin(models.AbstractModel):
    _name = "purchase.commission.mixin"
    _description = (
        "Mixin model for applying to any object that wants to handle commissions"
    )

    purchase_agent_ids = fields.One2many(
        comodel_name="purchase.commission.line.mixin",
        inverse_name="purchase_object_id",
        string="Purchase Agents & commissions",
        help="Agents/Commissions related to the invoice line.",
        compute="_compute_purchase_agent_ids",
        readonly=False,
        store=True,
        copy=True,
    )
    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    purchase_commission_free = fields.Boolean(
        string="Purchase Comm. free",
        related="product_id.purchase_commission_free",
        store=True,
        readonly=True,
    )
    purchase_commission_status = fields.Char(
        compute="_compute_purchase_commission_status", string="Purchase Commission",
    )

    def _prepare_agent_vals(self, purchase_agent):
        return {"purchase_agent_id": purchase_agent.id, "purchase_commission_id": purchase_agent.purchase_commission_id.id}

    def _prepare_agents_vals_partner(self, partner):
        """Utility method for getting agents creation dictionary of a partner."""
        return [(0, 0, self._prepare_agent_vals(purchase_agent)) for purchase_agent in partner.purchase_agent_ids]

    @api.depends("purchase_commission_free")
    def _compute_purchase_agent_ids(self):
        """Empty method that needs to be implemented in children models."""
        raise NotImplementedError()

    @api.depends("purchase_commission_free", "purchase_agent_ids")
    def _compute_purchase_commission_status(self):
        for line in self:
            if line.purchase_commission_free:
                line.purchase_commission_status = _("Comm. free")
            elif len(line.purchase_agent_ids) == 0:
                line.purchase_commission_status = _("No commission agents")
            elif len(line.purchase_agent_ids) == 1:
                line.purchase_commission_status = _("1 commission agent")
            else:
                line.purchase_commission_status = _("%s commission agents") % (
                    len(line.purchase_agent_ids),
                )

    def recompute_agents(self):
        self._compute_purchase_agent_ids()

    def button_edit_purchase_agents(self):
        self.ensure_one()
        view = self.env.ref("purchase_commission.view_purchase_commission_mixin_agent_only")
        return {
            "name": _("Purchase Agents"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": self._name,
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "res_id": self.id,
            "context": self.env.context,
        }


class PurchaseCommissionLineMixin(models.AbstractModel):
    _name = "purchase.commission.line.mixin"
    _description = (
        "Mixin model for having commission agent lines in "
        "any object inheriting from this one"
    )
    _rec_name = "purchase_agent_id"

    _sql_constraints = [
        (
            "unique_agent",
            "UNIQUE(purchase_object_id, purchase_agent_id)",
            "You can only add one time each agent.",
        )
    ]

    purchase_object_id = fields.Many2one(
        comodel_name="purchase.commission.mixin",
        ondelete="cascade",
        required=True,
        copy=False,
        string="Parent",
    )
    purchase_agent_id = fields.Many2one(
        comodel_name="res.partner",
        domain="[('purchase_agent', '=', True)]",
        ondelete="restrict",
        required=True,
    )
    purchase_commission_id = fields.Many2one(
        comodel_name="purchase.commission",
        ondelete="restrict",
        required=True,
        compute="_compute_commission_id",
        store=True,
        readonly=False,
        copy=True,
    )
    amount = fields.Monetary(
        string="Commission Amount", compute="_compute_amount", store=True,
    )
    # Fields to be overriden with proper source (via related or computed field)
    currency_id = fields.Many2one(comodel_name="res.currency")

    def _compute_amount(self):
        """Compute method to be implemented by inherited models."""
        raise NotImplementedError()

    def _get_commission_amount(self, commission, subtotal, product, quantity):
        """Get the commission amount for the data given. It's called by
        compute methods of children models.

        This means the inheritable method for modifying the amount of the commission.
        """
        self.ensure_one()
        if product.purchase_commission_free or not commission:
            return 0.0
        if commission.purchase_amount_base_type == "net_amount":
            # If subtotal (sale_price * quantity) is less than
            # standard_price * quantity, it means that we are selling at
            # lower price than we bought, so set amount_base to 0
            subtotal = max([0, subtotal - product.standard_price * quantity])
        if commission.purchase_commission_type == "fixed amount":
            return (commission.purchase_fix_qty * quantity)
        if commission.purchase_commission_type == "fixed":
            return subtotal * (commission.purchase_fix_qty / 100.0)
        elif commission.purchase_commission_type == "section":
            return commission.calculate_section(subtotal)

    @api.depends("purchase_agent_id")
    def _compute_commission_id(self):
        for record in self:
            record.purchase_commission_id = record.purchase_agent_id.purchase_commission_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: