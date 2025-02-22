from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class RoomBookingLine(models.Model):
    _name = "room.booking.line"
    _description = "Hotel Folio Line"
    _rec_name = 'room_id'

    @tools.ormcache()
    def _set_default_uom_id(self):
        return self.env.ref('uom.product_uom_day')

    booking_id = fields.Many2one("room.booking", string="Booking", help="Indicates the Room", ondelete="cascade")
    checkin_date = fields.Datetime(string="Check In", help="You can choose the date, Otherwise sets to current Date", required=True)
    checkout_date = fields.Datetime(string="Check Out", help="You can choose the date, Otherwise sets to current Date", required=True)
    room_id = fields.Many2one('hotel.room', string="Room", help="Indicates the Room", required=True)
    uom_qty = fields.Float(string="Duration", help="The quantity converted into the UoM used by the product", readonly=True)
    uom_id = fields.Many2one('uom.uom', default=_set_default_uom_id, string="Unit of Measure", help="This will set the unit of measure used", readonly=True)
    price_unit = fields.Float(string='Rent', related='room_id.list_price', digits='Product Price', help="The rent price of the selected room.")
    tax_ids = fields.Many2many('account.tax',
                               'hotel_room_order_line_taxes_rel',
                               'room_id', 'tax_id',
                               related='room_id.taxes_ids',
                               string='Taxes',
                               help="Default taxes used when selling the room.",
                               domain=[('type_tax_use', '=', 'sale')])
    currency_id = fields.Many2one(string='Currency', related='booking_id.currency_id', help='The currency used')
    price_subtotal = fields.Float(string="Subtotal", compute='_compute_price_subtotal', help="Total Price excluding Tax", store=True)
    price_tax = fields.Float(string="Total Tax", compute='_compute_price_subtotal', help="Tax Amount", store=True)
    price_total = fields.Float(string="Total", compute='_compute_price_subtotal', help="Total Price including Tax", store=True)
    state = fields.Selection(related='booking_id.state', string="Order Status", help=" Status of the Order", copy=False)
    booking_line_visible = fields.Boolean(default=False, string="Booking Line Visible", help="If True, then Booking Line will be visible")
    price_advance_payment = fields.Float(string="Advance Payment", related="booking_id.advanced_payment", readonly=False)
    no_of_person = fields.Integer(string="No of Person", related="room_id.num_person")
    extra_person = fields.Integer(string="Extra Person")
    discount = fields.Float(string="Discount")

    @api.onchange("checkin_date", "checkout_date")
    def _onchange_checkin_date(self):
        if self.checkout_date < self.checkin_date:
            raise ValidationError(_("Checkout must be greater or equal to check-in date"))
        if self.checkin_date and self.checkout_date:
            diffdate = self.checkout_date - self.checkin_date
            qty = diffdate.days
            if diffdate.total_seconds() > 0:
                qty += 1
            self.uom_qty = qty

    @api.depends('uom_qty', 'price_unit', 'tax_ids', 'price_advance_payment', 'discount')
    def _compute_price_subtotal(self):
        for line in self:
            price_subtotal = line.uom_qty * line.price_unit
            tax_results = line.tax_ids.compute_all(
                line.price_unit,
                currency=line.currency_id,
                quantity=line.uom_qty,
                partner=line.booking_id.partner_id
            )
            total_price = tax_results['total_included']
            if line.discount:
                total_price -= line.discount
            if line.price_advance_payment:
                total_price -= line.price_advance_payment
            line.price_subtotal = price_subtotal
            line.price_total = total_price
            line.price_tax = tax_results['total_included'] - tax_results['total_excluded']

    @api.onchange('checkin_date', 'checkout_date', 'room_id')
    def onchange_checkin_date(self):
        records = self.env['room.booking'].search([('state', 'in', ['reserved', 'check_in'])])
        for rec in records:
            rec_room_id = rec.room_line_ids.room_id
            rec_checkin_date = rec.room_line_ids.checkin_date
            rec_checkout_date = rec.room_line_ids.checkout_date
            if rec_room_id and rec_checkin_date and rec_checkout_date:
                for line in self:
                    if line.id != rec.id and line.room_id == rec_room_id:
                        if (rec_checkin_date <= line.checkin_date <= rec_checkout_date or rec_checkin_date <= line.checkout_date <= rec_checkout_date):
                            raise ValidationError(_("Sorry, You cannot create a reservation for this date since it overlaps with another reservation."))
                        if rec_checkout_date <= line.checkout_date and rec_checkin_date >= line.checkin_date:
                            raise ValidationError("Sorry, you cannot create a reservation for this date due to an existing reservation.")
