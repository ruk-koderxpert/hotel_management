from odoo import fields, models


class HelpdeskType(models.Model):
    _name = 'helpdesk.type'
    _description = 'Helpdesk Type'

    name = fields.Char(string='Type', help='Types of help desk.')
