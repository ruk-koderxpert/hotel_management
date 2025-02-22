from odoo import fields, models


class HotelService(models.Model):
    _name = 'hotel.service'
    _description = "Hotel Service"
    _inherit = 'mail.thread'
    _order = 'id desc'

    name = fields.Char(string="Service", help="Name of the service", required=True)
    unit_price = fields.Float(string="Price", help="Price of the service", default=0.0)
    taxes_ids = fields.Many2many('account.tax',
                                 'hotel_service_taxes_rel',
                                 'service_id', 'tax_id',
                                 string='Customer Taxes',
                                 help="Default taxes used when selling the service product.",
                                 domain=[('type_tax_use', '=', 'sale')],
                                 default=lambda self:self.env.company.account_sale_tax_id)
