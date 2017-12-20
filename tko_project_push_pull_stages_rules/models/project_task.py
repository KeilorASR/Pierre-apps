# -*- encoding: utf-8 -*-
##############################################################################
#
#    odoo, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    Thinkopen Brasil
#    Copyright (C) Thinkopen Solutions Brasil (<http://www.tkobr.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time

from odoo import SUPERUSER_ID
from odoo import fields, models, api, _
from odoo.exceptions import Warning
from odoo.osv import expression


class project_task_type(models.Model):
    _inherit = 'project.task.type'

    push_group_ids = fields.Many2many('res.groups', 'push_group_rel', 'push_group_id', 'task_type_id',
                                      string='Push Group')
    pull_group_ids = fields.Many2many('res.groups', 'pull_group_rel', 'pull_group_id', 'task_type_id',
                                      string='Push Group')
    push_rule = fields.Text('Push Rule')
    pull_rule = fields.Text('Pull Rule')
    pull_rule_filter_id = fields.Many2one('ir.filters', u'Pull Rule Filter')
    push_rule_filter_id = fields.Many2one('ir.filters',u'Push Rule Filter')
    push_server_action_id = fields.Many2one('ir.actions.server', string='Push Server Rule')
    pull_server_action_id = fields.Many2one('ir.actions.server', string='Pull Server Rule')
    pull_rule_warning_message = fields.Text('Pull Rule Warning Message')
    push_rule_warning_message = fields.Text('Push Rule Warning Message')

    @api.onchange('pull_rule_filter_id')
    def change_pull_rule_filter(self):
        self.pull_rule = self.pull_rule_filter_id.domain

    @api.onchange('push_rule_filter_id')
    def change_push_rule_filter(self):
        self.push_rule = self.push_rule_filter_id.domain


class project_task(models.Model):
    _inherit = 'project.task'

    # this method converts operator string in pythonic operator
    def compute_tuple(self, tup):
        if tup:
            operator = tup[1]
            tup_zero = tup[0]
            tup_two = tup[2]
            if tup_zero == '':
                tup_zero = False

            if tup_two == '':
                tup_two = False

            if operator == '=':
                result = tup_zero == tup_two

            elif operator == '!=' or operator == '<>':
                result = tup_zero != tup_two

            elif operator == 'in':
                result = tup_zero in tup_two

            elif operator == 'or' or operator == '||':
                result = tup_zero or tup_two

            elif operator == 'and' or operator == '&&':
                result = tup_zero and tup_two

            elif operator == 'not in':
                result = tup_zero not in tup_two

            elif operator == 'like':
                result = tup_zero in tup_two

            elif operator == '<':
                result = float(tup_zero) < float(tup_two)

            elif operator == '>':
                result = float(tup_zero) > float(tup_two)

            elif operator == '>=':
                result = float(tup_zero) >= float(tup_two)

            elif operator == '<=':
                result = float(tup_zero) <= float(tup_two)

            elif operator == 'ilike':
                result = str(tup_zero).lower() in str(tup_two).lower()
            else:
                raise Warning(_("Unsupported domain %s") % operator)

            return result

    def validate_domain(self, domain):
        if domain:
            if not isinstance(domain, list):
                raise Warning(_('Domain must be list'))
            # if it is single domain compute and return result
            if isinstance(domain, list) and len(domain) == 1:
                result = self.compute_tuple(domain[0])
                return result
            # domain is always a list
            if isinstance(domain, list) and len(domain) >= 3:
                pos_and = pos_or = False
                if '&' in domain:
                    pos_and = -domain[::-1].index('&') - 1
                if '|' in domain:
                    pos_or = -domain[::-1].index('|') - 1
                # compute most right operator and its index
                if pos_and and pos_or:
                    if pos_and > pos_or:
                        pos = pos_and
                        operator = 'and'
                    else:
                        pos = pos_or
                        operator = 'or'
                elif pos_and:
                    pos = pos_and
                    operator = 'and'

                elif pos_or:
                    pos = pos_or
                    operator = 'or'

                # replace tuples with True or False
                if isinstance(domain[pos + 1], tuple):
                    result = self.compute_tuple(domain[pos + 1])
                    domain[pos + 1] = result

                if isinstance(domain[pos + 2], tuple):
                    result = self.compute_tuple(domain[pos + 2])
                    domain[pos + 2] = result
                if operator == 'and':
                    new_value = domain[pos + 1] and domain[pos + 2]
                if operator == 'or':
                    new_value = domain[pos + 1] or domain[pos + 2]

                domain.remove(domain[pos])
                domain.remove(domain[pos + 1])
                domain.remove(domain[pos + 2])
                domain.append(new_value)

                if len(domain) >= 2:
                    self.validate_domain(domain)
        return domain[0]

    def _eval_context(self, uid, task_id, partner_id):
        """Returns a dictionary to use as evaluation context for
            domains."""
        return {
            'user': self.env.user,
            'time': time,
            'task_id': task_id,
            'partner_id': partner_id}

    def normalize(self, rule, user, partner, task):
        if rule:
            for tup in rule:
                index = rule.index(tup)
                if isinstance(tup, tuple):
                    left_conditon = tup[0]
                    if 'user' in left_conditon.split('.')[0] or 'task_id' in left_conditon.split('.')[0]:
                        for field_name in left_conditon.split('.'):
                            if field_name == 'user':
                                value = user
                            elif field_name == 'task_id':
                                value = task
                            elif field_name == 'time':
                                value = self._eval_context(user, task, partner)['time']
                            else:
                                try:
                                    value = value[field_name]
                                except:
                                    raise Warning(_("Field %s doesn't exist" % (field_name)))
                            rule[index] = (value, tup[1], tup[2])

        return rule

    @api.multi
    def write(self, vals):
        for record in self:
            validate_rules = True
            if self.env.uid == SUPERUSER_ID:
                validate_rules = False
            uid = self.env.uid
            user = self.env.user
            task = record
            if not record.partner_id:
                partner = self.env.user.partner_id
            else:
                partner = record.partner_id
            eval_context = self._eval_context(uid, task, partner)
            pre_pull_server_action_id = record.stage_id.pull_server_action_id
            if validate_rules:
                if 'stage_id' in vals.keys() and uid != SUPERUSER_ID:
                    target_stage = self.env['project.task.type'].browse(vals['stage_id'])
                    if record.stage_id.pull_rule and record.stage_id.name != target_stage.name:
                        try:
                            domain = eval(record.stage_id.pull_rule, eval_context)
                            if not isinstance(domain, list):
                                raise Warning(_('Domain must be list'))
                            pull_domain = expression.normalize_domain(domain)
                        except:
                            raise Warning(_('Please check condition for pull rule'))
                        # to compute left term of domain ( left terms are with quotes and are not normalized with method normalize_domain() of expression class
                        pull_domain = self.normalize(pull_domain, user, partner, task)
                        # validate domains
                        domain_result = self.validate_domain(pull_domain)
                        if not domain_result:
                            raise Warning(_('Pull rule is not validated, %s' % self.stage_id.pull_rule_warning_message))
                    if 'stage_id' in vals.keys():

                        # check push rule only if stage has not been changed, if write is called again
                        if target_stage.push_rule and record.stage_id.name != target_stage.name:
                            try:
                                domain = eval(target_stage.push_rule, eval_context)
                                if not isinstance(domain, list):
                                    raise Warning(_('Domain must be list'))
                                push_domain = expression.normalize_domain(domain)
                            except:
                                raise Warning(_('Please check condition for push rule'))
                            # to compute left term of domain ( left terms are with quotes and are not normalized with method normalize_domain() of expression class
                            push_domain = self.normalize(push_domain, user, partner, task)
                            # validate domains
                            domain_result = self.validate_domain(push_domain)
                            if not domain_result:
                                raise Warning(
                                    _('Push rule is not validated, %s' % target_stage.push_rule_warning_message))

                                # check rules before call super for pull
                    if record.stage_id.pull_group_ids:
                        pull_user = False
                        # set flag True if user found in pull_group_ids
                        for rule in record.stage_id.pull_group_ids:
                            for user in rule.users:
                                if user.id == uid:
                                    pull_user = True
                                    break
                        if not pull_user:
                            raise Warning(_('You are not allowed to pull task from this stage'))

            res = super(project_task, record).write(vals)

            if validate_rules and 'stage_id' in vals.keys() and uid != SUPERUSER_ID:
                # check rules before call super for push
                if record.stage_id.push_group_ids:
                    push_user = False
                    # set flag True if user found in push_group_ids
                    for rule in record.stage_id.push_group_ids:
                        for user in rule.users:
                            if user.id == uid:
                                push_user = True
                                break
                    if not push_user:
                        raise Warning(_('You are not allowed to push task to this stage'))

            # Execute server actions
            # active_id is not present in default context
            # server action fails with an error
            new_context = dict(self.env.context)
            if 'stage_id' in vals.keys():
                if 'active_id' not in new_context.keys():
                    new_context.update({'active_id':record.id})
                # run server actions:
                # execute only pull server action of source stage
                if pre_pull_server_action_id:
                    recs = pre_pull_server_action_id.with_context(new_context)
                    recs.run()
                # execute only push server action of target stage
                if record.stage_id.push_server_action_id:
                    recs = record.stage_id.push_server_action_id.with_context(new_context)
                    recs.run()
            return res
