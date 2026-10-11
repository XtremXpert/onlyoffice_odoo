from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons.onlyoffice_odoo_create.utils import MIMETYPES, build_blank


class OnlyofficeCreateWizard(models.TransientModel):
    _name = "onlyoffice.create.wizard"
    _description = "Créer un document ONLYOFFICE"

    name = fields.Char(
        string="Titre",
        required=True,
        default=lambda self: _("Nouveau document"),
    )
    doc_format = fields.Selection(
        selection=[
            ("docx", "Document Word (.docx)"),
            ("xlsx", "Feuille de calcul Excel (.xlsx)"),
            ("pptx", "Présentation PowerPoint (.pptx)"),
        ],
        string="Type",
        required=True,
        default="docx",
    )

    def action_create_open(self):
        self.ensure_one()
        title = (self.name or "").strip()
        if not title:
            raise UserError(_("Veuillez saisir un titre."))
        fmt = self.doc_format
        filename = title if title.lower().endswith("." + fmt) else f"{title}.{fmt}"
        attachment = self.env["ir.attachment"].create(
            {
                "name": filename,
                "raw": build_blank(fmt),
                "mimetype": MIMETYPES[fmt],
                "onlyoffice_created": True,
            }
        )
        return attachment.action_open_onlyoffice()
