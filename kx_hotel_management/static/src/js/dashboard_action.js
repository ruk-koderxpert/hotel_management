/** @odoo-module */
import { registry} from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, onMounted} = owl
import { rpc } from "@web/core/network/rpc";
import { Domain } from "@web/core/domain";
import { _t } from "@web/core/l10n/translation";
import {serializeDate,serializeDateTime,} from "@web/core/l10n/dates";
const today = new Date();
const day = today.getDate(); // Returns the day of the month (1-31)
const month = today.getMonth() + 1; // Returns the month (0-11); Adding 1 to match regular months (1-12)
const year = today.getFullYear(); // Returns the year (4 digits)
// Display the current date in a specific format (e.g., MM/DD/YYYY)
const formattedDate = `${year}-${month}-${day}`;
export class CustomDashBoard extends Component {
    /**
     * Setup method to initialize required services and register event handlers.
     */
setup() {
    this.action = useService("action");
    this.orm = useService("orm");
    onWillStart(this.onWillStart);
    onMounted(this.onMounted);
}
async onWillStart() {
    await this.fetch_data();
}
async onMounted() {
// Render other components after fetching data
// this.render_project_task();
// this.render_top_employees_graph();
// this.render_filter();
}
async fetch_data() {
        let result = await rpc('/web/dataset/call_kw/room.booking/get_details', {
            model: 'room.booking',
            method: 'get_details',
            args: [{}],
            kwargs: {},
        });

        this.total_room = result['total_room'];
        this.available_room = result['available_room'];
        this.staff = result['staff'];
        this.check_in = result['check_in'];
        this.reservation = result['reservation'];
        this.check_out = result['check_out'];
        this.total_vehicle = result['total_vehicle'];
        this.available_vehicle = result['available_vehicle'];
        this.total_event = result['total_event'];
        this.today_events = result['today_events'];
        this.pending_events = result['pending_events'];
        this.food_items = result['food_items'];
        this.food_order = result['food_order'];

        // Handle currency format
        if (result['currency_position'] === 'before') {
            this.total_revenue = result['currency_symbol'] + " " + result['total_revenue'];
            this.today_revenue = result['currency_symbol'] + " " + result['today_revenue'];
            this.pending_payment = result['currency_symbol'] + " " + result['pending_payment'];
        } else {
            this.total_revenue = result['total_revenue'] + " " + result['currency_symbol'];
            this.today_revenue = result['today_revenue'] + " " + result['currency_symbol'];
            this.pending_payment = result['pending_payment'] + " " + result['currency_symbol'];
        }
    }

    async markPaymentAsDone(bookingId) {
        await this.orm.call('room.booking', 'mark_payment_done', [[bookingId]]);
        // Refresh dashboard after payment
        await this.fetch_data();
    }
     total_rooms(e){
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options={on_reverse_breadcrum:this.on_reverse_breadcrum,};
                this.action.doAction({
                    name: _t("Rooms"),
                    type:'ir.actions.act_window',
                    res_model:'hotel.room',
                    view_mode:'list,form',
                    view_type:'form',
                    views:[[false,'list'],[false,'form']],
                    target:'current'
                },options)
    }
    check_ins(e){
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options={on_reverse_breadcrum:this.on_reverse_breadcrum,};
        this.action.doAction({
            name: _t("Check-In"),
            type:'ir.actions.act_window',
            res_model:'room.booking',
            view_mode:'list,form',
            view_type:'form',
            views:[[false,'list'],[false,'form']],
            domain: [['state', '=', 'check_in']],
            target:'current'
        },options)
    }
    //    Total Events
    view_total_events(e){
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options={on_reverse_breadcrum:this.on_reverse_breadcrum,};
        this.action.doAction({
            name: _t("Total Events"),
            type:'ir.actions.act_window',
            res_model:'event.event',
            view_mode:'kanban,list,form',
            view_type:'form',
            views:[[false,'kanban'],[false,'list'],[false,'form']],
            domain: [],
            target:'current'
        },options)
    }
//        //    Today's Events
    fetch_today_events(e){
        var today = new Date();
        var formattedDate = today.toISOString().split('T')[0];
        var startOfDay = formattedDate + " 00:00:00";
        var endOfDay = formattedDate + " 23:59:59";
        var options = { on_reverse_breadcrum: this.on_reverse_breadcrum };
        this.action.doAction({
            name: _t("Today's Events"),
            type: 'ir.actions.act_window',
            res_model: 'event.event',
            view_mode: 'kanban,list,form',
            view_type: 'form',
            views: [[false, 'kanban'], [false, 'list'], [false, 'form']],
            domain: [['date_end', '>=', startOfDay], ['date_end', '<=', endOfDay]],
            target: 'current'
        }, options);
    }
    fetch_pending_events(e){
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options={on_reverse_breadcrum:this.on_reverse_breadcrum,};
        this.action.doAction({
            name: _t("Pending Events"),
            type:'ir.actions.act_window',
            res_model:'event.event',
            view_mode:'kanban,list,form',
            view_type:'form',
            views:[[false,'kanban'],[false,'list'],[false,'form']],
            domain:  [['date_end', '>=', formattedDate]],
            target:'current'
        },options)
    }
//        //    Total staff
    fetch_total_staff(e){
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options={on_reverse_breadcrum:this.on_reverse_breadcrum,};
        this.action.doAction({
            name: _t("Total Staffs"),
            type:'ir.actions.act_window',
            res_model:'res.users',
            view_mode:'list,form',
            view_type:'form',
            views:[[false,'list'],[false,'form']],
            domain: [['groups_id.name', 'in',['Admin',
                       'Cleaning Team User',
                       'Cleaning Team Head',
                       'Receptionist',
                       'Maintenance Team User',
                       'Maintenance Team Leader'
                   ]]],
            target:'current'
        },options)
    }
    check_outs(e){
        var self = this;
        var options = { on_reverse_breadcrum: this.on_reverse_breadcrum };
        var today = new Date();
        var formattedDate = today.toISOString().split('T')[0];
        var startOfDay = formattedDate + " 00:00:00";
        var endOfDay = formattedDate + " 23:59:59";

        this.action.doAction({
            name: _t("Today's Check-Out"),
            type: 'ir.actions.act_window',
            res_model: 'room.booking',
            view_mode: 'list,form',
            view_type: 'form',
            views: [[false, 'list'], [false, 'form']],
            domain: [['room_line_ids.checkout_date', '>=', startOfDay], 
                     ['room_line_ids.checkout_date', '<=', endOfDay]],
            target: 'current'
        }, options);
    }
    available_rooms(e){
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options={on_reverse_breadcrum:this.on_reverse_breadcrum,};
        this.action.doAction({
            name: _t("Available Room"),
            type:'ir.actions.act_window',
            res_model:'hotel.room',
            view_mode:'list,form',
            view_type:'form',
            views:[[false,'list'],[false,'form']],
            domain: [['status', '=', 'available']],
            target:'current'
        },options)
    }
//    Reservations
    reservations(e){
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options={on_reverse_breadcrum:this.on_reverse_breadcrum,};
        this.action.doAction({
            name: _t("Total Reservations"),
            type:'ir.actions.act_window',
            res_model:'room.booking',
            view_mode:'list,form',
            view_type:'form',
            views:[[false,'list'],[false,'form']],
            domain: [['state', '=', 'reserved']],
            target:'current'
        },options)
    }
//    Food Items
    fetch_food_item(e){
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options={on_reverse_breadcrum:this.on_reverse_breadcrum,};
        this.action.doAction({
            name: _t("Food Items"),
            type:'ir.actions.act_window',
            res_model:'lunch.product',
            view_mode:'list,form',
            view_type:'form',
            views:[[false,'list'],[false,'form']],
            domain: [],
            target:'current'
        },options)
    }
//    food Orders
    async fetch_food_order(e){
        var self = this;
        const result = await this.orm.call('food.booking.line', 'search_food_orders',[{}],{});
        e.stopPropagation();
        e.preventDefault();
        var options={on_reverse_breadcrum:this.on_reverse_breadcrum,};
        this.action.doAction({
            name: _t("Food Orders"),
            type:'ir.actions.act_window',
            res_model:'food.booking.line',
            view_mode:'list,form',
            view_type:'form',
            views:[[false,'list'],[false,'form']],
           domain: [['id','in', result]],
            target:'current'
        },options)
    }
//    total vehicle
    fetch_total_vehicle(e){
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options={on_reverse_breadcrum:this.on_reverse_breadcrum,};
        this.action.doAction({name: _t("Total Vehicles"),
                    type:'ir.actions.act_window',
                    res_model:'fleet.vehicle.model',
                    view_mode:'list,form',
                    view_type:'form',
                    views:[[false,'list'],[false,'form']],
                    target:'current'
                },options)
    }
//    Available Vehicle
    async fetch_available_vehicle(e){
    const result = await this.orm.call('fleet.booking.line', 'search_available_vehicle',[{}],{});
        var self = this;
        var options={on_reverse_breadcrum:this.on_reverse_breadcrum,};
        e.stopPropagation();
        e.preventDefault();
        this.action.doAction({
            name: _t("Available Vehicle"),
            type:'ir.actions.act_window',
            res_model:'fleet.vehicle.model',
            view_mode:'list,form',
            view_type:'form',
            views:[[false,'list'],[false,'form']],
            domain: [['id','not in', result]],
            target:'current'
        },options)
    }
}
CustomDashBoard.template = "CustomDashBoard"
registry.category("actions").add("custom_dashboard_tags", CustomDashBoard);
