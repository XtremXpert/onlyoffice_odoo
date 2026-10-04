/** @odoo-module */
// Copyright (C) 2026 Ascensio System SIA

import { registry } from "@web/core/registry"
import { kanbanView } from "@web/views/kanban/kanban_view"
import { OnlyofficeKanbanController } from "./onlyoffice_kanban_controller"
import { OnlyofficeKanbanRenderer } from "./onlyoffice_kanban_renderer"

export const onlyofficeKanbanView = {
  ...kanbanView,
  // Odoo 20 : les boutons du panneau de contrôle sont un gabarit à part
  buttonTemplate: "onlyoffice_odoo_templates.KanbanView.Buttons",
  Controller: OnlyofficeKanbanController,
  Renderer: OnlyofficeKanbanRenderer,
}

registry.category("views").add("onlyoffice_kanban", onlyofficeKanbanView)
