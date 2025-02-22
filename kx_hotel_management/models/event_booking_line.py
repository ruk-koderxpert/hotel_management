from odoo import api, fields, models


class EventBookingLine(models.Model):
    _name = "event.booking.line"
    _description = "Hotel Event Line"
    _rec_name = 'event_id'

    booking_id = fields.Many2one("room.booking", string="Booking", help="Choose room booking reference", ondelete="cascade")
    event_id = fields.Many2one('event.event', string="Event", help="Choose the Event")
    ticket_id = fields.Many2one('product.product', string="Ticket", help="Choose the Ticket Type", domain=[('service_tracking', '=', 'event')])
    description = fields.Char(string='Description', help="Detailed description of the event", related='event_id.display_name')
    uom_qty = fields.Float(string="Quantity", default=1, help="The quantity converted into the UoM used by the product")
    uom_id = fields.Many2one('uom.uom', readonly=True, string="Unit of Measure", related='ticket_id.uom_id', help="This will set the unit of measure used")
    price_unit = fields.Float(related='ticket_id.lst_price', string='Price', digits='Product Price', help="The selling price of the selected ticket.")
    tax_ids = fields.Many2many('account.tax',
                               'hotel_event_order_line_taxes_rel',
                               'event_id',
                               'tax_id',
                               related='ticket_id.taxes_id',
                               string='Taxes',
                               help="Default taxes used when selling the event tickets.",
                               domain=[('type_tax_use', '=', 'sale')])
    currency_id = fields.Many2one(related='booking_id.pricelist_id.currency_id', string='Currency', help='The currency used', store=True, precompute=True)
    price_subtotal = fields.Float(string="Subtotal", compute='_compute_price_subtotal', help="Total Price Excluding Tax", store=True)
    price_tax = fields.Float(string="Total Tax", compute='_compute_price_subtotal', help="Tax Amount", store=True)
    price_total = fields.Float(string="Total", compute='_compute_price_subtotal', help="Total Price Including Tax", store=True)
    state = fields.Selection(related='booking_id.state', string="Order Status", help="State of Room Booking", copy=False)

    @api.depends('uom_qty', 'price_unit', 'tax_ids')
    def _compute_price_subtotal(self):
        for line in self:
            price_subtotal = line.uom_qty * line.price_unit            
            tax_results = line.tax_ids.compute_all(
                line.price_unit,
                currency=line.currency_id,
                quantity=line.uom_qty,
                partner=line.booking_id.partner_id
            )
            line.price_subtotal = price_subtotal
            line.price_total = tax_results['total_included']
            line.price_tax = tax_results['total_included'] - tax_results['total_excluded']

    def _prepare_base_line_for_taxes_computation(self):
        self.ensure_one()
        return self.env['account.tax']._prepare_base_line_for_taxes_computation(
            self,
            **{
                'tax_ids': self.tax_ids,
                'quantity': self.uom_qty,
                'partner_id': self.booking_id.partner_id,
                'currency_id': self.currency_id,
            },
        )
