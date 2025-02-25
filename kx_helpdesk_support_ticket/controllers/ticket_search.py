from odoo import http
from odoo.http import request


class TicketSearch(http.Controller):
    @http.route(['/ticketsearch'], type='json', auth="public", website=True)
    def ticket_search(self, **kwargs):
        """
        Search for tickets based on the provided search value.
        :param search_value: The value to search for in the ticket name or subject.
        :type search_value: str
        :return: A JSON response containing the matching tickets.
        :rtype: http.Response
        """
        search_value = kwargs.get("search_value")
        tickets = request.env["ticket.helpdesk"].search(['|', ('name', 'ilike', search_value), ('subject', 'ilike', search_value)])
        values = {'tickets': tickets}
        response = http.Response(template='kx_helpdesk_support_ticket.ticket_table', qcontext=values)
        return response.render()
