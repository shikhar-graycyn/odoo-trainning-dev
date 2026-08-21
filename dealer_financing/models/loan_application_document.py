from odoo import fields, models


class LoanApplicationDocument(models.Model):
    _name = "loan.application.document"
    _description = "Loan Application Document"

    name = fields.Char(string="Name")
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="Status",
        default="new",
    )
    type_id = fields.Many2one(
        comodel_name="loan.application.document.type", string="Document Type"
    )
    application_id = fields.Many2one(
        comodel_name="loan.application", string="Loan Application"
    )
    attachment_id = fields.Many2one(
        comodel_name="ir.attachment", string="Attachment"
    )

    def action_approve_document(self):
        self.state = "approved"

    def action_reject_document(self):
        self.state = "rejected"
