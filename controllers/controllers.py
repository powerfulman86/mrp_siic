# -*- coding: utf-8 -*-
# from odoo import http


# class MrpSiic(http.Controller):
#     @http.route('/mrp_siic/mrp_siic/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_siic/mrp_siic/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_siic.listing', {
#             'root': '/mrp_siic/mrp_siic',
#             'objects': http.request.env['mrp_siic.mrp_siic'].search([]),
#         })

#     @http.route('/mrp_siic/mrp_siic/objects/<model("mrp_siic.mrp_siic"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_siic.object', {
#             'object': obj
#         })
