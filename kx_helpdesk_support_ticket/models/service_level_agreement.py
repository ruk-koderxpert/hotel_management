from odoo import fields, models


class ServiceLevelAgreement(models.Model):
    _name = 'service.level.agreement'
    _description = 'Service Level Agreement'

    name = fields.Char(string='SLA', help='SLA name of the helpdesk.')
