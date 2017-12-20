# -*- coding: utf-8 -*-
{
    'name': "Project Timesheet Entry",
    'version': '1.0',
    'author': 'Aktiv Software',
    'website': 'http://www.aktivsoftware.com',
    'summary': 'Project User/Manager Enter Timesheet Entry By Wizard In Project Tasks And Issues',
    'category': 'Project',
    'license': 'AGPL-3',
    'depends': ['project_issue_sheet'],
    'description': """
        This module helps to project user and manager ,to fill up timesheet of project's task and issue quickly by a wizard(pop-up).
        Project user has only creating and reading rights of timesheet, while the manager can access everything.
        """,
    'data': [
            'security/ir.model.access.csv',
            'wizard/project_view_wizard.xml',
            'views/project.xml', ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
