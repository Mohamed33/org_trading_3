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

from odoo import api, models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        imediate_obj = self.env['stock.immediate.transfer']
        res = super(PurchaseOrder, self).button_confirm()
        params = self.env['ir.config_parameter'].sudo()
        is_delivery_set_to_done_purchase = bool(params.get_param('is_delivery_set_to_done_purchase'))
        create_invoice_purchase = bool(params.get_param('create_invoice_purchase'))
        validate_invoice_purchase = bool(params.get_param('validate_invoice_purchase'))

        for order in self:
            if is_delivery_set_to_done_purchase and order.picking_ids:
                for picking in self.picking_ids:
                    picking.action_assign()
                    picking.action_confirm()
                    for mv in picking.move_ids_without_package:
                        mv.quantity_done = mv.product_uom_qty
                    picking.button_validate()

            if create_invoice_purchase and not order.invoice_ids:
                order.action_create_invoice()

            if validate_invoice_purchase and order.invoice_ids:
                for invoice in order.invoice_ids:
                    invoice.action_post()

        return res
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

