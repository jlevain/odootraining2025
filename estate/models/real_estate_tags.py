from odoo import models, fields

class RealEstateTags(models.Model):
    _name = "real.estate.tags"
    _description = 'Real Estate Tags'

    name = fields.Char(default="Tags", required=True)