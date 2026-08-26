from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    loan_application_ids = fields.One2many(
        comodel_name="loan.application",
        inverse_name="sale_order_id",
        string="Loan Applications",
    )
    loan_application_count = fields.Integer(
        string="Loan Applications",
        compute="_compute_loan_application_count",
    )

    @api.depends("loan_application_ids")
    def _compute_loan_application_count(self):
        for order in self:
            order.loan_application_count = len(order.loan_application_ids)

    def action_create_loan(self):
        self.ensure_one()
        financeable_lines = self.order_line.filtered(
            lambda line: line.product_id
            and line.product_id.product_tmpl_id.is_financeable
        )

        if not financeable_lines:
            raise UserError(
                self.env._(
                    "The sale order must contain exactly one financeable product."
                )
            )
        if len(financeable_lines) > 1:
            raise UserError(
                self.env._(
                    "The sale order cannot contain more than one financeable "
                    "product."
                )
            )

        financeable_line = financeable_lines[0]
        context = dict(self.env.context)
        context.update(
            {
                "default_sale_order_id": self.id,
                "default_partner_id": self.partner_id.id,
                "default_product_id": (
                    financeable_line.product_id.product_tmpl_id.id
                ),
                "default_principal_amount": financeable_line.price_subtotal,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Loan Application"),
            "res_model": "loan.application",
            "view_mode": "form",
            "target": "current",
            "context": context,
        }

    def action_view_loan_applications(self):
        self.ensure_one()
        context = dict(self.env.context)
        context.update(
            {
                "default_sale_order_id": self.id,
                "default_partner_id": self.partner_id.id,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Loan Applications"),
            "res_model": "loan.application",
            "view_mode": "list,form",
            "target": "current",
            "domain": [("sale_order_id", "=", self.id)],
            "context": context,
        }
