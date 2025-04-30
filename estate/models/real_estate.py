from odoo import models, fields
from datetime import date, time, datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging
import random

class RealEstate(models.Model):
    _name = "real.estate"
    _description: str = 'Real Estate'

    name = fields.Char(default="House", required=True)
    description = fields.Text()
    postcode = fields.Char()

    addmonths = date.today() + relativedelta(months=3)
    date_availability = fields.Date(string="Date de disponibilité", default=addmonths, copy=False)

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
    active = fields.Boolean(active=True)
    state = fields.Selection(
        selection = [
            ("N", "New"),
            ("OR", "Offer Received"),
            ("OA", "Offer Accepted"),
            ("S", "Sold"),
            ("C", "Canceled"),
        ], 
        string='Status', 
        required=True
        )
    property_type_id = fields.Many2one("real.estate.type", string="Type")
    buyer_id = fields.Many2one('res.partner', required=True, string='Buyer', index=True)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
