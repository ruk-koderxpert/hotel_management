from odoo import models


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    def _compute_visible(self):
        super()._compute_visible()
        show_menu_header = self.env['ir.config_parameter'].sudo().get_param('kx_helpdesk_support_ticket.helpdesk_menu_show')
        for menu in self:
            if menu.name == 'Helpdesk' and not show_menu_header:
                menu.is_visible = False
            if menu.name == 'Helpdesk' and show_menu_header:
                menu.is_visible = True
