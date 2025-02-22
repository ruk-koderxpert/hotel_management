from odoo import fields, models

class HotelRoomImage(models.Model):
    _name = 'hotel.room.image'
    _description = 'Hotel Room Images'
    # _order = 'sequence, id'

    name = fields.Char("Name", required=True)
    image = fields.Image("Image", max_width=1920, max_height=1920, required=True)
    seq = fields.Integer("Sequence", default=10)
    room_id = fields.Many2one('hotel.room', string="Room", required=True, ondelete='cascade')
