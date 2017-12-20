from odoo import api, fields, models

class ProjectTaskType(models.Model):

    _inherit = 'project.task.type'

    visible_ts_btn = fields.Boolean(string='Timesheet Button Visibility',help="If you want hide 'Fill up Timesheet' Button in Project's task & issue stage",default=True)

class Task(models.Model):

    _inherit = 'project.task'

    visible_ts_btn = fields.Boolean(related='stage_id.visible_ts_btn',string='Button Visibility',help="If you want hide 'Fill up Timesheet' Button in Project's task & issue stage",store=True)

class ProjectIssue(models.Model):
    _inherit = "project.issue"

    visible_ts_btn = fields.Boolean(related='stage_id.visible_ts_btn',string='Button Visibility',help="If you want hide 'Fill up Timesheet' Button in Project's task & issue stage",store=True)