# -*- coding: utf-8 -*-
from odoo import models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def write(self, vals):
        res = super().write(vals)
        if (
            'standard_price' in vals and
            not self.env.context.get('sync_standard_price_all_companies')
        ):
            companies = self.env['res.company'].search([])
            for template in self:
                for company in companies:
                    current_cost = template.with_company(company).standard_price
                    if current_cost != vals['standard_price']:
                        template.with_company(company).with_context(sync_standard_price_all_companies=True).standard_price = vals['standard_price']
        return res

