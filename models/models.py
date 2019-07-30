# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class exp_default(models.Model):
#     _name = 'exp_default.exp_default'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

# class DefaultMember(models.Model):
#     _inherit = 'res.partner'
#     _name = 'member.default'
#     # Fields
#     name = fields.Char(string='Order References', required=True, copy=False, readonly=True)
#     sale_ok = fields.Boolean('Can be sold', defalt=True, help="Check if the product can be sold")
#     sequence = fields.Integer('Sequences', default=1)
#     discount = fields.Float(string='Discount (%)', digit=dp.get_precision('Discount'))
#     amount = fields.Monetary(currency_fields='currency_id')
#     term = fields.Text('Terms and Conditions')
#     state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], required=True)
#     note = fields.Html('Note')
#     date_invoiced = fields.Date(string='Invoice Date')
#     date_done = fields.Datetime(string='Closed Done')
#     data_file = fields.Binary(string='Bank Statement File')
#     partner_id = fields.Many2one('res.partner', string='costumer', change_default=True, index=True, track_visibility='always')
#     order_line = fields.One2many('sale.order.line', 'order.id', string='Order Lines')
#     tags_ids = fields.Many2many('crm.lead.tag', 'crm_lead_tag_rel', 'lead_id', 'tag_id', string='Tags')
#     document_id = fields.Reference(selection=get_document_types, string='Source Document', required=True)

class Course(models.Model):
    _name = 'member.course'

    name = fields.Char(string='Judul', required=True)
    description = fields.Text()
    session_ids = fields.One2many('member.session', 'course_id', String='Sesi')
    responsible_id = fields.Many2one('res.users', on_delete='set null', string='Penanggung Jawab', index=True)

class Session(models.Model):
    _name = 'member.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6,2), help='Durasi Hari')
    seats = fields.Integer(string='Jumlah Kursi')
    instructor_id = fields.Many2one('res.partner', string='Instruktur')
    course_id = fields.Many2one('member.course', on_delete='cascade', String='Kursus', required=True)
    attendees_ids = fields.Many2many('res.partner', string='Peserta')
