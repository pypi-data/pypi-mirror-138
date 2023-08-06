from odoo import api, fields, models


class SubscribtionRequest(models.Model):
    _inherit = "subscription.request"

    sepa_approved = fields.Boolean(string="Approved SEPA")
