from odoo import api, fields, models, tools


class FleetBookingLine(models.Model):
    _name = "fleet.booking.line"
    _description = "Hotel Fleet Line"
    _rec_name = 'fleet_id'

    @tools.ormcache()
    def _get_default_uom_id(self):
        return self.env.ref('uom.product_uom_km')

    booking_id = fields.Many2one("room.booking", string="Booking", ondelete="cascade", help="Shows the room Booking")
    fleet_id = fields.Many2one('fleet.vehicle.model', string="Vehicle", help='Indicates the Vehicle')
    description = fields.Char(string='Description', related='fleet_id.display_name', help="Description of Vehicle")
    uom_qty = fields.Float(string="Total KM", default=1, help="The quantity converted into the UoM used by the product")
    uom_id = fields.Many2one('uom.uom', readonly=True, string="Unit of Measure", default=_get_default_uom_id, help="This will set the unit of measure used")
    price_unit = fields.Float(string='Rent/KM', related='fleet_id.price_per_km', digits='Product Price', help="The rent/km of the selected fleet.")
    tax_ids = fields.Many2many('account.tax',
                               'hotel_fleet_order_line_taxes_rel',
                               'fleet_id',
                               'tax_id',
                               string='Taxes',
                               help="Default taxes used when renting the fleet models.",
                               domain=[('type_tax_use', '=', 'sale')])
    currency_id = fields.Many2one(related='booking_id.pricelist_id.currency_id', string="Currency", help='The currency used')
    price_subtotal = fields.Float(string="Subtotal", compute='_compute_price_subtotal', help="Total price excluding tax", store=True)
    price_tax = fields.Float(string="Total Tax", compute='_compute_price_subtotal', help="Total tax amount", store=True)
    price_total = fields.Float(string="Total", compute='_compute_price_subtotal', help="Total Price Including Tax", store=True)
    state = fields.Selection(related='booking_id.state', string="Order Status", help=" Status of the Order", copy=False)

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

    def search_available_vehicle(self):
        return (self.env['fleet.vehicle.model'].search([('id', 'in', self.search([]).mapped('fleet_id').ids)]).ids)
