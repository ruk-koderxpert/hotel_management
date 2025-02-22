from odoo import api, fields, models, tools


class FoodBookingLine(models.Model):
    _name = "food.booking.line"
    _description = "Hotel Food Line"
    _rec_name = 'food_id'

    @tools.ormcache()
    def _get_default_uom_id(self):
        return self.env.ref('uom.product_uom_unit')

    booking_id = fields.Many2one(
        "room.booking", string="Booking", help="Shows the room Booking", ondelete="cascade")
    food_id = fields.Many2one(
        'lunch.product', string="Product", help="Indicates the Food Product")
    description = fields.Char(
        string='Description', help="Description of Food Product", related='food_id.display_name')
    uom_qty = fields.Float(string="Qty", default=1,
                            help="The quantity converted into the UoM used by the product")
    uom_id = fields.Many2one('uom.uom', readonly=True, string="Unit of Measure",
                            default=_get_default_uom_id, help="This will set the unit of measure used")
    price_unit = fields.Float(related='food_id.price', string='Price',
                            digits='Product Price', help="The price of the selected food item.")
    tax_ids = fields.Many2many('account.tax',
                            'hotel_food_order_line_taxes_rel',
                            'food_id', 'tax_id',
                            string='Taxes',
                            help="Default taxes used when selling the food products.",
                            domain=[('type_tax_use', '=', 'sale')])
    currency_id = fields.Many2one(
        related='booking_id.pricelist_id.currency_id', string="Currency", help='The currency used')
    price_subtotal = fields.Float(
        string="Subtotal", compute='_compute_price_subtotal', help="Total Price Excluding Tax", store=True)
    price_tax = fields.Float(
        string="Total Tax", compute='_compute_price_subtotal', help="Tax Amount", store=True)
    price_total = fields.Float(
        string="Total", compute='_compute_price_subtotal', help="Total Price Including Tax", store=True)
    state = fields.Selection(related='booking_id.state',
                            string="Order Status", help=" Status of the Order", copy=False)

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
            line.price_tax = tax_results['total_included'] - \
                tax_results['total_excluded']

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

    def search_food_orders(self):
        return (self.search([]).filtered(lambda r: r.booking_id.state not in ['check_out', 'cancel', 'done']).ids)
