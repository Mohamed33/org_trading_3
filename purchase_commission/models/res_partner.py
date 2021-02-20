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


class ResPartner(models.Model):
    """Add some fields related to commissions"""

    _inherit = "res.partner"

    purchase_agent_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="partner_agent_rel",
        column1="partner_id",
        column2="purchase_agent_id",
        domain=[("purchase_agent", "=", True)],
        readonly=False,
        string="Purchase Agents",
    )
    # Fields for the partner when it acts as an agent
    purchase_agent = fields.Boolean(
        string="Purchase Creditor/Agent",
        help="Check this field if the partner is a creditor or an agent.",
    )
    purchase_agent_type = fields.Selection(
        selection=[("agent", "External agent")], string=" Purchase Agent Type", default="agent",
    )
    purchase_commission_id = fields.Many2one(
        string="Purchase Commission",
        comodel_name="purchase.commission",
        help="This is the default commission used in the purchase where this "
        "agent is assigned. It can be changed on each operation if "
        "needed.",
    )
    settlement = fields.Selection(
        selection=[
            ("monthly", "Monthly"),
            ("quaterly", "Quarterly"),
            ("semi", "Semi-annual"),
            ("annual", "Annual"),
        ],
        string="Settlement period",
        default="monthly",
    )
    purchase_settlement_ids = fields.One2many(
        comodel_name="purchase.commission.settlement",
        inverse_name="purchase_agent_id",
        readonly=True,
    )

    @api.model
    def _commercial_fields(self):
        """Add agents to commercial fields that are synced from parent to childs."""
        res = super()._commercial_fields()
        res.append("purchase_agent_ids")
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: