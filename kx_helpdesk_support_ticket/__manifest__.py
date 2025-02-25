{
    'name': "Helpdesk Support Ticket",
    'version': '17.0.1.0.1',
    'category': 'Website',
    'summary': """The Helpdesk Support Ticket module enables users to create support tickets from the website, manage them in the backend, and generate service charge-based invoices.""",
    'description': """
Helpdesk Support Ticket
==========================================
- Ticket Creation
- Backend Management
- Service Charge Invoices
- Automated Notifications
- Security & Access Control
- Reporting
    """,
    'author':'KoderXpert Technologies LLP',
    'company': 'KoderXpert Technologies LLP',
    'maintainer': 'KoderXpert Technologies LLP',
    'website': 'https://koderxpert.com',
    'depends': ['website', 'project', 'sale_project', 'hr_timesheet', 'mail', 'contacts'],
    'data': [
        'security/website_helpdesk_groups.xml',
        'security/website_helpdesk_security.xml',
        'security/ir.model.access.csv',
        'data/helpdesk_category_data.xml',
        'data/helpdesk_replay_template_data.xml',
        'data/helpdesk_type_data.xml',
        'data/ir_cron_data.xml',
        'data/ir_sequence_data.xml',
        'data/mail_template_data.xml',
        'data/ticket_stage_data.xml',
        'views/ticket_helpdesk_views.xml',
        'views/team_helpdesk_views.xml',
        'views/helpdesk_category_views.xml',
        'views/helpdesk_tag_views.xml',
        'views/helpdesk_type_views.xml',
        'views/merge_ticket_views.xml',
        'views/website_helpdesk_portal_templates.xml',
        'views/portal_templates.xml',
        'views/rating_form.xml',
        'report/helpdesk_ticket_report_template.xml',
        'report/report_action.xml',
        'views/res_config_settings_views.xml',
        'views/ticket_stage_views.xml',
        'views/website_form.xml',
        'views/service_level_agreement_views.xml',
        'views/ticket_status_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/static/src/js/ticket_details.js',
            '/static/src/js/portal_search.js',
            '/static/src/js/multiple_product_choose.js',
        ]
    },
    'images': ['static/description/kx_helpdesk_support_ticket.gif'],
    'price': 50,
    'currency': 'USD',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
