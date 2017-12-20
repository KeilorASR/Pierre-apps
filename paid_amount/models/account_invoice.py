# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    _description = "Account Invoice Paid Amounts"

    paid_amount = fields.Monetary(string='Paid Amount',
                               compute='_compute_paid_amount', store=True, help="The Paid Amount.")

    @api.one
    @api.depends('residual')
    def _compute_paid_amount(self):
        self.paid_amount = self.amount_total - self.residual

    # @api.one
    # @api.depends(
    #     'state', 'currency_id', 'invoice_line_ids.price_subtotal',
    #     'move_id.line_ids.amount_residual',
    #     'move_id.line_ids.currency_id')
    # def _compute_residual(self):
    #     res = super(AccountInvoice, self)._compute_residual()
    #     self.paid_amount = self.amount_total - self.residual
    #     return res