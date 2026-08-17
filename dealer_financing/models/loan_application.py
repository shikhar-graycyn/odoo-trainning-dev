from odoo import fields, models


class LoanApplication(models.Model):
    _name = "loan.application"
    _description = "Loan Application"

    name = fields.Char(string="Application Number", required=True)
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Customer", required=True
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    product_id = fields.Many2one(
        comodel_name="product.template", string="Motorcycle"
    )
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency")
    loan_amount = fields.Monetary(
        string="Loan Amount", currency_field="currency_id", required=True
    )
    down_payment = fields.Monetary(
        string="Down Payment", currency_field="currency_id"
    )
    loan_term = fields.Integer(string="Term (Months)", default=36)
    interest_rate = fields.Float(
        string="Interest Rate", digits=(5, 2), required=True
    )
    date_applied = fields.Date(
        string="Application Date", default=lambda self: fields.Date.today()
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("credit_check", "Credit Check"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("signed", "Signed"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        default="draft",
        copy=False,
    )
    active = fields.Boolean(default=True)
    notes = fields.Html(string="Internal Notes", copy=False)
