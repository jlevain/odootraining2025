from odoo import models, fields, api, _
from datetime import date, time, datetime, timedelta
from pprint import pprint
from dateutil.relativedelta import relativedelta
import logging
import random

from odoo.addons.test_import_export.models.models_export_impex import compute_fn
from odoo.exceptions import RedirectWarning, UserError


class RealEstate(models.Model):
    _name = "real.estate"
    _description: str = 'Real Estate'

    name = fields.Char(default="House", required=True)
    description = fields.Text()
    postcode = fields.Char()

    addmonths = date.today() + relativedelta(months=3)
    date_availability = fields.Date(string="Date de disponibilité", default=addmonths, copy=False)

    tag_ids = fields.Many2many("real.estate.tags", string="Tags")

    offer_ids = fields.One2many("real.estate.offer", "real_estate_id", string="Offers")

    best_price = fields.Float(
        string="Best price", store=False,
        compute='_compute_bestprice',
    )

    expected_price = fields.Float()
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [
            ("N", "North"),
            ("S", "South"),
            ("E", "East"),
            ("W", "West"),
    ], string='Garden Orientation')
    total_area = fields.Float(
        string="Total area", store=True,
        compute='_compute_area',
        default=0
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection = [
            ("N", "New"),
            ("OR", "Offer Received"),
            ("OA", "Offer Accepted"),
            ("S", "Sold"),
            ("C", "Canceled"),
        ], 
        string='Status', 
        required=True,
        default="N"
        )
    property_type_id = fields.Many2one("real.estate.type", string="Type")
    buyer_id = fields.Many2one('res.partner', required=True, string='Buyer', index=True)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)

    @api.depends("garden", "living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            if record.garden:
                record.total_area = record.living_area + record.garden_area
            else:
                record.total_area = record.living_area

    @api.onchange("garden", "garden_area", "garden_orientation")
    def _onchange_garden(self):
        if self.garden and not self.garden_area:
            self.garden_area = 10
            self.garden_orientation = "N"

    @api.depends("offer_ids.price")
    def _compute_bestprice(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids.mapped('price') else None

    def sold(self):
        if self.state == "C":
            raise UserError(_("Offer already CANCELED"))
            #raise RedirectWarning("l'offre est déjà CANCELED", 'action', "Show ")
        if self.state != "C":
            self.state = "S"
        return True

    @api.depends('state')
    def cancel(self):
        if self.state == "S":
            raise UserError(_("Offer already SOLD"))
        if self.state != "S":
            self.state = "C"
        return True