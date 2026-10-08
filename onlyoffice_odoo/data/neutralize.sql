-- Neutralized copy (staging): never reach the production Document Server, nor
-- ONLYOFFICE's demo server, and never sign tokens the production accepts. The
-- Document Server would otherwise call back the production Odoo
-- (doc_server_odoo_url) and could save a staging edit on a production attachment.
DELETE FROM ir_config_parameter
 WHERE key IN ('onlyoffice_connector.doc_server_public_url',
               'onlyoffice_connector.doc_server_inner_url',
               'onlyoffice_connector.doc_server_odoo_url',
               'onlyoffice_connector.doc_server_jwt_secret',
               'onlyoffice_connector.internal_jwt_secret',
               'onlyoffice_connector.doc_server_demo',
               'onlyoffice_connector.doc_server_demo_date');
