# -*- coding: utf-8 -*-
from odoo import http

# class ExpDefault(http.Controller):
#     @http.route('/exp_default/exp_default/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exp_default/exp_default/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('exp_default.listing', {
#             'root': '/exp_default/exp_default',
#             'objects': http.request.env['exp_default.exp_default'].search([]),
#         })

#     @http.route('/exp_default/exp_default/objects/<model("exp_default.exp_default"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exp_default.object', {
#             'object': obj
#         })