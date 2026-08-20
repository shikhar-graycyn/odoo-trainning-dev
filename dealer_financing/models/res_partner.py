from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    loan_application_ids = fields.One2many(
        comodel_name="loan.application",
        inverse_name="partner_id",
        string="Loan Application Records",
    )
    loan_application_count = fields.Integer(
        string="Loan Applications",
        compute="_compute_loan_application_count",
    )

    @api.depends("loan_application_ids", "loan_application_ids.active")
    def _compute_loan_application_count(self):
        for partner in self:
            partner.loan_application_count = len(partner.loan_application_ids)

    def action_view_loan_applications(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Loan Applications"),
            "res_model": "loan.application",
            "view_mode": "list,form",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }
