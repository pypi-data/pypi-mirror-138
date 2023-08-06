# -*- coding: utf-8 -*-
from odoo.http import request
from odoo.addons.easy_my_coop_website.controllers.main import WebsiteSubscription
from odoo import http
from odoo.http import request
from datetime import datetime


class WebsiteSubscription(WebsiteSubscription):

    def fill_values(self, values, is_company, logged, load_from_user=False):
        values = super(WebsiteSubscription, self).fill_values(values, is_company, logged, load_from_user=False)
        sub_req_obj = request.env['subscription.request']
        fields_desc = sub_req_obj.sudo().fields_get(['sepa_approved'])
        comp = request.env["res.company"]._company_default_get()
        values.update({
            "display_sepa_approval": comp.display_sepa_approval,
            "sepa_approval_text": comp.sepa_approval_text,
        })
        return values
