from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LoanApplication(models.Model):
    _name = "loan.application"
    _description = "Loan Application"

    name = fields.Char(string="Application Number", required=True)
    partner_id = fields.Many2one(
        "res.partner", string="Customer", required=True
    )
    email = fields.Char(string="Email", related="partner_id.email")
    phone = fields.Char(string="Phone", related="partner_id.phone")
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    product_id = fields.Many2one(
        comodel_name="product.template", string="Motorcycle"
    )
    tag_ids = fields.Many2many(
        comodel_name="loan.application.tag", string="Tags"
    )
    document_ids = fields.One2many(
        comodel_name="loan.application.document",
        inverse_name="application_id",
        string="Documents",
    )
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency")
    principal_amount = fields.Monetary(
        string="Principal Amount", currency_field="currency_id"
    )
    down_payment = fields.Monetary(
        string="Down Payment", currency_field="currency_id"
    )
    loan_amount = fields.Monetary(
        string="Loan Amount",
        currency_field="currency_id",
        compute="_compute_loan_amount",
        inverse="_inverse_loan_amount",
    )
    loan_term = fields.Integer(string="Term (Months)", default=36)
    interest_rate = fields.Float(
         digits=(5, 2), required=True
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

    _name_unique = models.Constraint(
        "unique(name)",
        "Loan application reference must be unique.",
    )
    _principal_positive = models.Constraint(
        "CHECK(principal_amount > 0)",
        "Principal amount must be greater than zero.",
    )

    @api.depends("principal_amount", "down_payment")
    def _compute_loan_amount(self):
        for record in self:
            record.loan_amount = record.principal_amount - record.down_payment

    def _inverse_loan_amount(self):
        for record in self:
            record.down_payment = record.principal_amount - record.loan_amount

    @api.constrains("principal_amount", "down_payment")
    def _check_down_payment(self):
        for record in self:
            if record.down_payment >= record.principal_amount:
                raise ValidationError(
                    self.env._(
                        "Down payment must be less than the principal amount."
                    )
                )
