from odoo import models, fields

class RealEstateType(models.Model):
    _name = "real.estate.type"
    _description = 'Real Estate Type'
    _order = "sequence, name, id"

    name = fields.Char(default="Type", required=True)
    sequence = fields.Integer('Sequence', default=1, help="")

    offer_ids = fields.One2many("real.estate.offer", "real_estate_id", string="Offers")

    property_ids = fields.One2many("real.estate", "property_type_id", string="Offres")

    _sql_constraints = [
        (
            'unique_tag_name',
            'unique(name)',  # Nom technique de la contrainte
            'Le type doit être unique.'  # Message d’erreur affiché à l’utilisateur
        ),
    ]