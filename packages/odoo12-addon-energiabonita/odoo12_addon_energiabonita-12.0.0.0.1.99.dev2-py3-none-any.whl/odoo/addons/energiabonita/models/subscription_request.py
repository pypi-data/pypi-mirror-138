from odoo import api, fields, models


class SubscribtionRequest(models.Model):
    _inherit = "subscription.request"

    sepa_approved = fields.Boolean(string="Approved SEPA")

    def get_required_field(self):
        req_fields = super(SubscribtionRequest, self).get_required_field()
        company = self.env["res.company"]._company_default_get()
        if company.sepa_approval_required:
            req_fields.append("sepa_approved")
        return req_fields
