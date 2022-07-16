# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpUnbuild(models.Model):
    _inherit = 'mrp.unbuild'

    @api.model
    def _get_branch(self):
        if self.env.user.branch_id:
            return self.env.user.branch_id.id
        else:
            return self.env['res.branch'].search([], limit=1, order='id').id

    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch", required=True, readonly=True, tracking=1,
                                index=True, help='This is branch to set', states={'draft': [('readonly', False)]},
                                default=_get_branch)
    mo_id = fields.Many2one(
        'mrp.production', 'Manufacturing Order',
        domain="[('state', 'in', ['done', 'cancel']), ('company_id', '=', company_id),('branch_id','=',branch_id)]",
        states={'done': [('readonly', True)]}, check_company=True)
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id),('branch_id','=',branch_id)]",
        check_company=True,
        required=True, states={'done': [('readonly', True)]}, help="Location where the product you want to unbuild is.")
    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location',
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id),('branch_id','=',branch_id)]",
        check_company=True,
        required=True, states={'done': [('readonly', True)]},
        help="Location where you want to send the components resulting from the unbuild order.")

    @api.onchange('mo_id')
    def _onchange_mo_id(self):
        if self.mo_id:
            self.product_id = self.mo_id.product_id.id
            self.product_qty = self.mo_id.product_qty
            self.product_uom_id = self.mo_id.product_uom_id
            self.bom_id = self.mo_id.bom_id
            self.location_id = self.mo_id.location_dest_id
            self.location_dest_id = self.mo_id.location_id
