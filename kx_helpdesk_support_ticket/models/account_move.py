from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    ticket_id = fields.Many2one('ticket.helpdesk', string='Ticket', help='ID of the ticket.')
