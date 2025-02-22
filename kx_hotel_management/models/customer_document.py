from odoo import fields, models


class CustomerDocument(models.Model):
    _name = "customer.document"
    _description = "Customer Dcoument"

    name = fields.Char('Document Name')
    attachment_ids = fields.Many2many("ir.attachment")
    booking_id = fields.Many2one("room.booking", string="Room Booking", ondelete="cascade")