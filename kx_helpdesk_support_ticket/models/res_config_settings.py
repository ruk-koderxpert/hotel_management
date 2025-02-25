from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_create_task = fields.Boolean(string="Create Tasks",
                                      config_parameter='kx_helpdesk_support_ticket.show_create_task',
                                      help='Enable this option to allow users'
                                           'to create tasks directly from the '
                                           'helpdesk module. When activated, users '
                                           'will have the ability to generate and '
                                           'assign tasks as part of their workflow '
                                           'within the helpdesk interface.')
    show_category = fields.Boolean(string="Category",
                                   config_parameter='kx_helpdesk_support_ticket.show_category',
                                   help='Enable this option to display the '
                                        'category field in the helpdesk tickets. '
                                        'This can be useful for organizing and '
                                        'filtering tickets based on their category.',
                                   implied_group='kx_helpdesk_support_ticket.group_show_category')
    product_website = fields.Boolean(string="Product On Website",
                                     config_parameter='kx_helpdesk_support_ticket.product_website',
                                     help='Product on website')
    auto_close_ticket = fields.Boolean(string="Auto Close Ticket",
                                       config_parameter='kx_helpdesk_support_ticket.auto_close_ticket',
                                       help='Auto Close ticket')
    no_of_days = fields.Integer(string="No Of Days",
                                config_parameter='kx_helpdesk_support_ticket.no_of_days',
                                help='No of Days')
    closed_stage_id = fields.Many2one('ticket.stage', string='Closing stage',
                                      help='Closing Stage of the ticket.',
                                      config_parameter='kx_helpdesk_support_ticket.closed_stage_id')

    reply_template_id = fields.Many2one('mail.template',
                                        domain="[('model', '=', 'ticket.helpdesk')]",
                                        config_parameter='kx_helpdesk_support_ticket.reply_template_id',
                                        help='Reply Template of the helpdesk ticket.')
    helpdesk_menu_show = fields.Boolean('Helpdesk Menu',
                                        config_parameter='kx_helpdesk_support_ticket.helpdesk_menu_show',
                                        help='Helpdesk menu')

    @api.onchange('closed_stage_id')
    def _onchange_closed_stage_id(self):
        """Closing stage function"""
        if self.closed_stage_id:
            stage = self.closed_stage_id.id
            in_stage = self.env['ticket.stage'].browse(stage)
            in_stage.write({'closing_stage': True})
            self.env['ticket.stage'].search([('id', '!=', stage)]).write({'closing_stage': False})

    @api.constrains('show_category')
    def _constrains_show_category_subcategory(self):
        """Show category and the sub category"""
        if self.show_category:
            group_cat = self.env.ref('kx_helpdesk_support_ticket.group_show_category')
            group_cat.users = [(4, self.env.user.id)]
        else:
            group_cat = self.env.ref('kx_helpdesk_support_ticket.group_show_category')
            group_cat.users = [(5, self.env.user.id)]
