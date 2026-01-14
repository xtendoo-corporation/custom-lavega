from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ProductSyncWizard(models.TransientModel):
    _name = "product.sync.wizard"
    _description = "Sincronizar costes e impuestos entre compañías"

    company_src_id = fields.Many2one('res.company', string="Compañía Origen", required=True)
    company_dst_id = fields.Many2one('res.company', string="Compañía Destino", required=True)

    def action_sync_products(self):
        #Propagamos costes de productos entre compañías
        if self.company_src_id == self.company_dst_id:
            _logger.warning("Sincronización cancelada: la compañía origen y destino son la misma (%s)", self.company_src_id.name)
            return {'type': 'ir.actions.act_window_close'}
        # Buscar todos los productos
        tmpl_srcs = self.env['product.template'].search([])
        if not tmpl_srcs:
            _logger.warning("No se encontraron productos para sincronizar.")
            return {'type': 'ir.actions.act_window_close'}
        count_updated = 0
        for tmpl in tmpl_srcs:
            coste_src = tmpl.with_company(self.company_src_id).standard_price
            coste_dst = tmpl.with_company(self.company_dst_id).standard_price
            _logger.info("ANTES: '%s' en '%s': coste=%.2f", tmpl.name, self.company_dst_id.name, coste_dst)
            # Propagar el coste de la compañía origen a la destino
            tmpl.with_company(self.company_dst_id).write({'standard_price': coste_src})
            _logger.info("DESPUÉS: '%s' en '%s': coste=%.2f", tmpl.name, self.company_dst_id.name, tmpl.with_company(self.company_dst_id).standard_price)
            count_updated += 1
        _logger.info("Sincronización finalizada: %d productos actualizados en destino.", count_updated)
        return {'type': 'ir.actions.act_window_close'}
