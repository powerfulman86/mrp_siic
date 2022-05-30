# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def _get_default_picking_type(self):
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self.env.user.branch_id:
            return self.env['stock.picking.type'].search([
                ('code', '=', 'mrp_operation'),
                ('warehouse_id.company_id', '=', company_id),
                ('warehouse_id.branch_id', '=', self.env.user.branch_id.id),
            ], limit=1).id
        else:
            return self.env['stock.picking.type'].search([
                ('code', '=', 'mrp_operation'),
                ('warehouse_id.company_id', '=', company_id)
            ], limit=1).id

    @api.model
    def _get_default_location_src_id(self):
        location = False
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self.env.context.get('default_picking_type_id'):
            location = self.env['stock.picking.type'].browse(
                self.env.context['default_picking_type_id']).default_location_src_id
        if not location:
            location = self.env['stock.warehouse'].search(
                [('company_id', '=', company_id), ('branch_id', '=', self.branch_id.id)], limit=1).lot_stock_id
        return location and location.id or False

    @api.model
    def _get_default_location_dest_id(self):
        location = False
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self._context.get('default_picking_type_id'):
            location = self.env['stock.picking.type'].browse(
                self.env.context['default_picking_type_id']).default_location_dest_id
        if not location:
            location = self.env['stock.warehouse'].search(
                [('company_id', '=', company_id), ('branch_id', '=', self.branch_id.id)], limit=1).lot_stock_id
        return location and location.id or False

    @api.model
    def _get_branch(self):
        if self.env.user.branch_id:
            return self.env.user.branch_id.id
        else:
            return self.env['res.branch'].search([], limit=1, order='id').id

    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch", required=True, readonly=True, tracking=1,
                                index=True, help='This is branch to set', states={'draft': [('readonly', False)]},
                                default=_get_branch)

    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
        domain="[('code', '=', 'mrp_operation'), ('company_id', '=', company_id),('branch_id','=',branch_id)]",
        default=_get_default_picking_type, required=True, check_company=True)

    location_src_id = fields.Many2one(
        'stock.location', 'Components Location',
        default=_get_default_location_src_id,
        readonly=True, required=True,
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id),('branch_id','=',branch_id)]",
        states={'draft': [('readonly', False)]}, check_company=True,
        help="Location where the system will look for components.")
    location_dest_id = fields.Many2one(
        'stock.location', 'Finished Products Location',
        default=_get_default_location_dest_id,
        readonly=True, required=True,
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id),('branch_id','=',branch_id)]",
        states={'draft': [('readonly', False)]}, check_company=True,
        help="Location where the system will stock the finished products.")

    @api.onchange('branch_id')
    def onchange_branch_id(self):
        new_picking = self.env['stock.picking.type'].search(
            [('code', '=', 'mrp_operation'), ('branch_id', '=', self.branch_id.id)], limit=1)
        self.picking_type_id = new_picking
