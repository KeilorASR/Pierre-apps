# -*- coding: utf-8 -*-

from datetime import datetime
from openerp import api, fields, models, _


#Add Project Task Wizard With Work Log,Duration Field And Write Method For Task Timesheet.
class ProjectTaskWizard(models.TransientModel):
    _name = 'project.task.wizard'

    name = fields.Text(string="Work Log")
    duration = fields.Float(string="Duration")
    
    @api.multi
    def write_task_log(self):
        """
        Button method to write timesheet lines in tasks using button.
        -------------------------------------------------------------
        @param self: object pointer
        """
        record_id = self.env.context and self.env.context.get('active_id', False) or False
        pt_obj = self.env['project.task']
        project_task = pt_obj.browse(record_id)
        project_task.sudo().write({
            'timesheet_ids': [(0, 0, {
                'date': datetime.now(),
                'user_id': self._uid,
                'name': self.name,
                'unit_amount': float(self.duration),
                'account_id':project_task.project_id.analytic_account_id.id,
                'project_id': project_task.project_id.id
             })]   
        })
        ms = _("Task timesheet fillup by %s.") % (self.env.user.name)
        project_task.message_post(body=ms)
        return True

#Add Project Issue Wizard With Work Log,Duration Field And Write Method For Issue Timesheet.
class ProjectIssueWizard(models.TransientModel):
    _name = 'project.issue.wizard'

    name = fields.Text(string="Work Log")
    duration = fields.Float(string="Duration")
    
    @api.multi
    def write_issue_log(self):
        """
        Button method to write timesheet lines in issues using button.
        --------------------------------------------------------------
        @param self: object pointer
        """
        record_id = self.env.context and self.env.context.get('active_id', False) or False
        pt_obj = self.env['project.issue']
        project_issue = pt_obj.browse(record_id)
        project_issue.sudo().write({
            'timesheet_ids': [(0, 0, {
                'date': datetime.now(),
                'user_id': self._uid,
                'name': self.name,
                'unit_amount': float(self.duration),
                'account_id':project_issue.project_id.analytic_account_id.id,
                'project_id': project_issue.project_id.id
             })]
        })
        ms = _("Issue timesheet fillup by %s.") % (self.env.user.name)
        project_issue.message_post(body=ms) 
        return True        