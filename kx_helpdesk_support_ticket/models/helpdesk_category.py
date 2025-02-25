from odoo import fields, models


class HelpdeskCategory(models.Model):
    _name = 'helpdesk.category'
    _description = 'Categories'

    name = fields.Char('Name', help='Category name of the helpdesk')
    sequence = fields.Integer('Sequence', default=0, help='Sequence of the helpdesk category')
