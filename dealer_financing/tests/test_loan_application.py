from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase


class TestLoanApplication(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {"name": "Dealer Financing Test Customer"}
        )
        cls.required_document_type = cls.env[
            "loan.application.document.type"
        ].create(
            {
                "name": "Dealer Financing Test Required Document",
                "is_required": True,
                "active": True,
            }
        )

    def _valid_loan_vals(self, **overrides):
        vals = {
            "name": "TEST-LOAN-BASE",
            "partner_id": self.partner.id,
            "currency_id": self.env.company.currency_id.id,
            "principal_amount": 10_000.0,
            "down_payment": 2_000.0,
            "interest_rate": 8.5,
        }
        vals.update(overrides)
        return vals

    def test_01_computes_and_crud(self):
        loan = self.env["loan.application"].create(
            self._valid_loan_vals(name="TEST-LOAN-COMPUTE")
        )

        self.assertEqual(loan.loan_amount, 8_000.0)
        self.assertTrue(loan.document_ids)

    def test_02_python_constraints(self):
        with self.assertRaises(ValidationError):
            self.env["loan.application"].create(
                self._valid_loan_vals(
                    name="TEST-LOAN-CONSTRAINT",
                    principal_amount=5_000.0,
                    down_payment=10_000.0,
                )
            )

    def test_03_workflow_user_error(self):
        loan = self.env["loan.application"].create(
            self._valid_loan_vals(name="TEST-LOAN-SUBMISSION")
        )
        required_document = loan.document_ids.filtered(
            lambda document: (
                document.type_id == self.required_document_type
                and document.state != "approved"
            )
        )

        self.assertTrue(required_document)
        with self.assertRaises(UserError):
            loan.action_submit()
