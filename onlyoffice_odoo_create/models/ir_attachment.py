from odoo import fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    onlyoffice_created = fields.Boolean(
        string="Créé via ONLYOFFICE",
        default=False,
        index=True,
        help="Document vierge créé depuis l'assistant « Nouveau document » ONLYOFFICE.",
    )

    def action_open_onlyoffice(self):
        """Ouvre la pièce jointe dans l'éditeur ONLYOFFICE (nouvel onglet)."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": "/onlyoffice/editor/%d" % self.id,
            "target": "new",
        }
