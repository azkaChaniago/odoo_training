from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'member.wizard'

    def _default_session(self):
        blah =  self.env['member.session'].browse(self._context.get('active_ids'))
        print '+++++++++++++++++++++++++++++++++', blah
        return blah

    session_id = fields.Many2one('member.session', string='Sesi', required=True, default=_default_session)
    attendees_ids = fields.Many2many('res.partner', string='Peserta')

    sessions_ids = fields.Many2many('member.session', string='Sesi')

    @api.multi
    def add_attendance(self):
        self.session_id.attendees_ids |= self.attendees_ids
        return {}

    @api.multi
    def add_multiple_attendance(self):
            for sesi in self.sessions_ids:
                sesi.attendees_ids |= self.attendees_ids
            return {}
