from odoo import api, fields, models, tools


class ServiceBookingLine(models.Model):
    _name = "service.booking.line"
    _description = "Hotel service Line"

    @tools.ormcache()
    def _get_default_uom_id(self):
        return self.env.ref('uom.product_uom_unit')

    booking_id = fields.Many2one("room.booking", string="Booking", help="Indicates the Room Booking", ondelete="cascade")
    service_id = fields.Many2one('hotel.service', string="Service", help="Indicates the Service")
    description = fields.Char(string='Description', related='service_id.name', help="Description of the Service")
    uom_qty = fields.Float(string="Qty", default=1.0, help="The quantity converted into the UoM used by the product")
    uom_id = fields.Many2one('uom.uom', readonly=True, string="Unit of Measure", help="This will set the unit of measure used", default=_get_default_uom_id)
    price_unit = fields.Float(string='Price', related='service_id.unit_price', digits='Product Price', help="The price of the selected service.")
    tax_ids = fields.Many2many('account.tax',
                               'hotel_service_order_line_taxes_rel',
                               'service_id', 'tax_id',
                               related='service_id.taxes_ids',
                               string='Taxes',
                               help="Default taxes used when selling the services.",
                               domain=[('type_tax_use', '=', 'sale')])
    currency_id = fields.Many2one(string='Currency', related='booking_id.pricelist_id.currency_id', help='The currency used')
    price_subtotal = fields.Float(string="Subtotal", compute='_compute_price_subtotal', help="Total Price Excluding Tax", store=True)
    price_tax = fields.Float(string="Total Tax", compute='_compute_price_subtotal', help="Tax Amount", store=True)
    price_total = fields.Float(string="Total", compute='_compute_price_subtotal', help="Total Price Including Tax", store=True)
    state = fields.Selection(related='booking_id.state', string="Order Status", help=" Status of the Order", copy=False)
    booking_line_visible = fields.Boolean(default=False, string="Booking Line Visible", help="If true, Booking line will be visible")

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
