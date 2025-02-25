from odoo import fields, models


class HelpdeskTag(models.Model):
    _name = 'helpdesk.tag'
    _description = 'Helpdesk Tags'

    name = fields.Char(string='Tag', help='Tag name of the helpdesk.')
