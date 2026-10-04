/** @odoo-module **/
// Copyright (C) 2026 Ascensio System SIA

import { Dialog } from "@web/core/dialog/dialog"
import { _t } from "@web/core/l10n/translation"

import { Component, t, useProps } from "@odoo/owl"

export class HelpDialog extends Component {
  props = useProps({ close: t.function().optional() })

  setup() {
    this.title = _t("Help")
  }
}

HelpDialog.template = "onlyoffice_odoo_templates.HelpDialog"
HelpDialog.components = { Dialog }
