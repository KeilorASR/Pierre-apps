# -*- coding: utf-8 -*-
# © 2016 Jérôme Guerriat
# © 2016 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo import fields
from odoo import api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    customer_name = fields.Char(related='partner_id.name')

    @api.multi
    def name_get(self):
        result = []
        for project in self:
            name = project.name
            if project.partner_id:
                name = project.partner_id.name + ' - ' + name

            result.append((project.id, name))

        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name),
                      ('customer_name', operator, name)]
        projects = self.search(domain + args, limit=limit)
        if projects:
            return projects.name_get()
        return super(ProjectProject, self).name_search(name, args, operator,
                                                       limit)
