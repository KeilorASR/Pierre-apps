# -*- coding: utf-8 -*-
##############################################
#
# Difusión Visual
# Copyright (C) Difusión Visual
# all rights reserved
# http://difusionvisual.com
# contacto@difusionvisual.com
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/> or
# write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################


from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = "product.template"

    recommend_price = fields.Float(string='Recommend Price', store=True)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    recommend_price = fields.Float(string='Recommend Price', related='product_id.recommend_price', store=True)


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    recommend_price = fields.Float(string='Recommend Price', related='product_id.recommend_price', store=True)


class StockPackOperation(models.Model):
    _inherit = "stock.pack.operation"

    recommend_price = fields.Float(string='Recommend Price', related='product_id.recommend_price', store=True)


class StockMove(models.Model):
    _inherit = 'stock.move'

    recommend_price = fields.Float(string='Recommend Price', related='product_id.recommend_price', store=True)


class ResCompany(models.Model):
    _inherit = 'res.company'

    recommend_bool = fields.Boolean(string='Show Recommend Price', store=True)





