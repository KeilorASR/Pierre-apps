# -*- coding: utf-8 -*-
# © 2016 Jérôme Guerriat
# © 2016 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Project - Customer name',
    'category': 'Project',
    'summary': 'Add customer name to project tiles',
    'website': 'https://www.niboo.be/',
    'version': '10.0.1.0',
    'description': """
        With this module, you can easily keep track on which project belongs to which client.
        """,
    'author': 'Niboo',
    'depends': [
        'project',
    ],
    'data': [
        'views/project_dashboard.xml'
    ],
    'images': [
        'static/description/project_customer_name_cover.png',
    ],
    'installable': True,
    'application': False,
}
