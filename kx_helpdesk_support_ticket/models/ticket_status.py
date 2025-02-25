from odoo import fields, models


class TicketStatus(models.Model):
    _name = 'ticket.status'
    _description = 'Ticket Status'

    name = fields.Char(string='Ticket Status', help='Ticket Status of the helpdesk.')
