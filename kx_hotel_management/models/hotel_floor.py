from odoo import fields, models


class HotelFloor(models.Model):
    _name = "hotel.floor"
    _description = "Floor"
    _order = 'id desc'

    name = fields.Char(string="Name", help="Name of the floor", required=True)
    user_id = fields.Many2one('res.users', string='Manager', help="Manager of the Floor", required=True)
