from odoo import fields, models


class LoanApplicationTag(models.Model):
    _name = "loan.application.tag"
    _description = "Loan Application Tag"

    name = fields.Char(string="Name")
    color = fields.Integer(string="Color")
