# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Subject(models.Model):
    _name = 'member.subject'

    name = fields.Char(string='Subject Name')
    description = fields.Text()
    instructor_id = fields.Many2Many('res.partner',
                                    string='Instruktur',
                                    domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Pengajar')])
    