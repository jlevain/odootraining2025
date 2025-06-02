from odoo import models, fields

class RealEstateTags(models.Model):
    _name = "real.estate.tags"
    _description = 'Real Estate Tags'
    _order = "name asc"

    name = fields.Char(default="Tags", required=True)
    color = fields.Integer()

    _sql_constraints = [
        (
            'unique_tag_name',
            'unique(name)',  # Nom technique de la contrainte
            'Le nom du tag doit être unique.'  # Message d’erreur affiché à l’utilisateur
        ),
    ]