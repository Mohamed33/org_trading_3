from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    lot_ids = fields.Many2many('stock.production.lot', string="Crate", copy=False)

    @api.model
    def create(self, vals):
        res = super(StockMove, self).create(vals)
        if res and res.sale_line_id and res.lot_ids:
            prod_uom_qty = res.product_uom_qty
            lines = []
            if self.product_id.tracking == 'serial':
                for lot in res.lot_ids:
                    if prod_uom_qty > 0:
                        lines.append((0, 0, {'lot_id': lot.id,
                                             'qty_done': 1,
                                             'product_uom_id': res.product_uom.id,
                                             'picking_id': res.picking_id.id,
                                             'move_id': res.id,
                                             'product_id': res.product_id.id,
                                             'location_id': res.location_id.id,
                                             'location_dest_id': res.location_dest_id.id}))
                    prod_uom_qty -= 1
            if self.product_id.tracking == 'lot':
                lines.append((0, 0, {'lot_id': res.lot_ids[0].id,
                                     'qty_done': res.product_uom_qty,
                                     'product_uom_id': res.product_uom.id,
                                     'picking_id': res.picking_id.id,
                                     'move_id': res.id,
                                     'product_id': res.product_id.id,
                                     'location_id': res.location_id.id,
                                     'location_dest_id': res.location_dest_id.id}))
            if lines:
                res.write({'move_line_ids': lines})
        return res
