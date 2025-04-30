from odoo import models, fields

class RealEstateType(models.Model):
    _name = "real.estate.type"
    _description = 'Real Estate Type'

    name = fields.Char(default="Type", required=True)