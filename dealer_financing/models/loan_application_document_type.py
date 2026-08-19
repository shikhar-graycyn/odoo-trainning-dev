from odoo import fields, models


class LoanApplicationDocumentType(models.Model):
    _name = "loan.application.document.type"
    _description = "Loan Application Document Type"

    name = fields.Char(string="Name")
    is_required = fields.Boolean(string="Required")
    active = fields.Boolean(default=True)
