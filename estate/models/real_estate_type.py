from odoo import models, fields

class RealEstateType(models.Model):
    _name = "real.estate.type"
    _description = 'Real Estate Type'

    name = fields.Char(default="Type", required=True)

    offer_ids = fields.One2many("real.estate.offer", "real_estate_id", string="Offers")

    _sql_constraints = [
        (
            'unique_tag_name',
            'unique(name)',  # Nom technique de la contrainte
            'Le type doit être unique.'  # Message d’erreur affiché à l’utilisateur
        ),
    ]