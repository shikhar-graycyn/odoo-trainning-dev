from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_financeable = fields.Boolean(
        string="Financeable",
        default=False,
    )
