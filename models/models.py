# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta

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

    name = fields.Char(string='Judul', required=True, readonly=True, states={'draft': [('readonly', False)]})
    description = fields.Text(readonly=True, states={'draft': [('readonly', False)]})
    session_ids = fields.One2many('member.session', 'course_id', String='Sesi', readonly=True, states={'draft': [('readonly', False)]})
    responsible_id = fields.Many2one('res.users',
                                    on_delete='set null',
                                    string='Penanggung Jawab',
                                    index=True,
                                    readonly=True,
                                    states={'draft': [('readonly', False)]})

    _sql_constraints = [
        ('name_description_check', 'CHECK(name != description)', 'Course Name and descriptions aren\'t suppose to be same'),
        ('name_unique', 'UNIQUE(name)', 'Course name should be unique')
    ]

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count([('name', '=like', 'Copy of {}%'.format(self.name))])
        if not copied_count:
            new_name = 'Copy of {}'.format(self.name)
        else:
            new_name = 'Copy of {} ({})'.format(self.name, copied_count)
        default['name'] = new_name
        return super(Course, self).copy(default)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('done', 'Done'),
    ], string='Status', readonly=True, copy=False, default='draft')

    @api.multi
    def action_confirm(self):
        self.write({ 'state': 'open' })

    @api.multi
    def action_cancel(self):
        self.write({ 'state': 'draft' })

    @api.multi
    def action_close(self):
        self.write({ 'state': 'done' })

class Session(models.Model):
    _name = 'member.session'

    name = fields.Char(required=True)
    start_date = fields.Date(string='Tanggal Mulai', default=fields.Date.today)
    duration = fields.Float(digits=(6,2), help='Durasi Hari')
    seats = fields.Integer(string='Jumlah Kursi')
    course_id = fields.Many2one('member.course', on_delete='cascade', string='Kursus', required=True)
    instructor_id = fields.Many2one('res.partner',
                                    string='Instruktur',
                                    domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Pengajar')])
    attendees_ids = fields.Many2many('res.partner', string='Peserta', domain=[('instructor', '=', False)])
    taken_seats = fields.Float(string='Kursi Terisi', compute='_taken_seats')
    end_date = fields.Date(string='Tanggal Selesai', store=True, compute='_get_end_date', inverse='_set_end_date')
    attendees_count = fields.Integer(string='Jumlah Peserta', compute='_get_attendees_count', store=True)
    color = fields.Integer('Warna')

    @api.depends('seats', 'attendees_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendees_ids) / r.seats

    @api.onchange('seats', 'attendees_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'value': {
                    'seats': len(self.attendees_ids) or 1
                },
                'warning': {
                    'title': 'TOTAL SEAT INVALID',
                    'message': 'Seat/\'s total must be positive'
                }
            }
        if self.seats < len(self.attendees_ids):
            return {
                'value': {
                    'seats': len(self.attendees_ids)
                },
                'warning': {
                    'title': 'PARTICIPANTS ARE OVERLOADED',
                    'message': 'Add seats or decrease participants or attendees'
                }
            }

    @api.constrains('instructor_id', 'attendees_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendees_ids:
                raise exceptions.ValidationError('An instructor aren\'t allowed to be attendant')   

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration
    
    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1

    @api.depends('attendees_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendees_ids)