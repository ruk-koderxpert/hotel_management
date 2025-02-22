from odoo import http
from odoo.http import request
from datetime import datetime, timedelta

class HotelBooking(http.Controller):
    @http.route(['/hotel/room/<int:room_id>/book'], type='http', auth="public", website=True)
    def room_booking(self, room_id, **post):
        room = request.env['hotel.room'].sudo().browse(room_id)
        values = {
            'room': room,
            'page_name': 'booking_form',
        }
        if post:
            customer = request.env['res.partner'].sudo().search([('email', '=', post.get('email'))], limit=1)
            if not customer:
                customer = request.env['res.partner'].sudo().create({
                    'name': post.get('name'),
                    'email': post.get('email'),
                    'phone': post.get('mobile'),
                    'street': post.get('address'),
                })
            
            checkin_date = post.get('date')
            checkout_date = (datetime.strptime(checkin_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

            booking_vals = {
                'email': post.get('email'),
                'mobile': post.get('mobile'),
                'address': post.get('address'),
                'aadhar_card': post.get('aadhar_number'),
                'date_order': checkin_date,
                'partner_id': customer.id,
                'room_line_ids': [(0, 0, {
                    'room_id': room.id,
                    'checkin_date': checkin_date,
                    'checkout_date': checkout_date,
                })]
            }

            booking = request.env['room.booking'].sudo().create(booking_vals)
            return request.redirect('/booking/confirmation/%s' % booking.id)
        return request.render("kx_hotel_management.booking_form", values)

    @http.route(['/booking/confirmation/<int:booking_id>'], type='http', auth="public", website=True)
    def booking_confirmation(self, booking_id, **post):
        return request.render("kx_hotel_management.booking_confirmation")
