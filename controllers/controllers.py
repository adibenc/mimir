# -*- coding: utf-8 -*-
# from odoo import http


# class BaseNetworkManagement(http.Controller):
#     @http.route('/mimir/mimir', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mimir/mimir/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mimir.listing', {
#             'root': '/mimir/mimir',
#             'objects': http.request.env['mimir.mimir'].search([]),
#         })

#     @http.route('/mimir/mimir/objects/<model("mimir.mimir"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mimir.object', {
#             'object': obj
#         })

