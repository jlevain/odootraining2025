from email.policy import default
from odoo import models, fields, api
from datetime import date, time, datetime, timedelta
from dateutil.relativedelta import relativedelta


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
        for record in self:
            record.status = "A"
            record.selling_price = ''
        return True

    @api.depends("status")
    def offer_refused(self):
        for record in self:
            record.status = "R"
        return True