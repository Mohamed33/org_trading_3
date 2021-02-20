# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    lot_ids = fields.Many2many('stock.production.lot', string='Lot', copy=False)

    def _create_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._create_stock_moves(picking)
        res['lot_ids'] = [(6, 0, self.lot_ids.ids)]
        return res
