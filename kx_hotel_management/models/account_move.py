from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    hotel_booking_id = fields.Many2one('room.booking', string="Booking Reference", readonly=True, help="Choose the Booking Reference")
