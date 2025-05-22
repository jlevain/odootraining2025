from email.policy import default
from odoo import models, fields, api, _
from datetime import date, time, datetime, timedelta
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)

from odoo.exceptions import UserError, ValidationError

class RealEstateOffer(models.Model):
    _name = "real.estate.offer"
    _description = 'Offer'

    name = fields.Char(default="Offer", required=True)
    price = fields.Float()

    validity = fields.Integer(default=30)

    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_deadline',
        inverse='_compute_validity'
    )

    status = fields.Selection(
        selection=[
            ("A", "Accepted"),
            ("R", "Refused"),
        ], string='Status', copy=False)

    partner_id = fields.Many2one('res.partner', required=True)
    real_estate_id = fields.Many2one("real.estate", required=True)


    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            createDate = record.create_date if record.create_date else datetime.now()
            record.date_deadline = createDate + timedelta(days=record.validity)

    @api.depends("create_date", "validity")
    def _compute_validity(self):
        for record in self:
            #if record.date_deadline:
            dateDeadline = (record.date_deadline - record.create_date.date())
            record.validity = dateDeadline.days

    @api.depends("status")
    def offer_accepted(self):
        #import ipdb
        #ipdb.set_trace()
        #_logger.debug("DEBUG")

        for record in self:
            res_already_accepted = record.real_estate_id.offer_ids.filtered(lambda o: o.status == "A")
            if res_already_accepted:
                raise ValidationError(_("An offer has been already accepted"))
            res_filtered = record.real_estate_id.offer_ids.filtered(lambda o: o.status != "A")
            if res_filtered and record:
                res_filtered.status = "R"
            record.status = "A"
            record.real_estate_id.buyer_id = record.partner_id
        return True

    @api.depends("status")
    def offer_refused(self):
        for record in self:
            record.status = "R"
        return True

    @api.constrains('price')
    def _check_expected_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("Field price must be positiv")

    @api.constrains('status', 'real_estate_id')
    def _check_real_estate_id(self):
        for record in self:
            if record.status and record.status == "A" and record.real_estate_id.expected_price > 0:
                limit_to_sell = record.real_estate_id.expected_price * 0.9
                if record.price <= limit_to_sell:
                    raise ValidationError("Selling price is too low (more than 10%)")