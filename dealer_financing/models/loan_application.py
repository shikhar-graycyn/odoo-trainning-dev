from odoo import fields, models


class LoanApplication(models.Model):
    _name = "loan.application"
    _description = "Loan Application"

    name = fields.Char(string="Application Number", required=True)
    loan_term = fields.Integer(string="Term (Months)", default=36)
    interest_rate = fields.Float(string="Interest Rate", digits=(5, 2))
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
    )
    active = fields.Boolean(default=True)
    notes = fields.Html(string="Internal Notes")
