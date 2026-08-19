# Project Structure

## Overview

This development environment runs Odoo 19 from source and combines three addon
locations:

```text
/home/shikhar_gc/
├── odoo/                    Odoo Community server and standard addons
├── odoo-enterprise/         Odoo Enterprise addons
└── odoo-trainning-dev/      Project-specific custom addons
    └── dealer_financing/    Dealer Financing application
```

The Community repository provides the Odoo server (`odoo-bin`). Enterprise is
an additional addon collection and is not started as a separate server.

## Addon Loading Order

The active configuration is stored in `/home/shikhar_gc/odoo/odoo.conf`.
Its addon paths are ordered as follows:

```ini
addons_path = /home/shikhar_gc/odoo-enterprise,/home/shikhar_gc/odoo/addons,/home/shikhar_gc/odoo-trainning-dev
```

1. `odoo-enterprise` loads Enterprise overrides and applications first.
2. `odoo/addons` provides the standard Community applications.
3. `odoo-trainning-dev` provides locally developed custom applications.

## Repository Responsibilities

### `odoo`

- Odoo 19 Community source code.
- Contains the `odoo-bin` server entry point.
- Contains the Python virtual environment in `venv/`.
- Contains the local runtime configuration in `odoo.conf`.
- Should generally remain aligned with the upstream `19.0` branch.

### `odoo-enterprise`

- Odoo 19 Enterprise addon source code.
- Must use the same version branch as the Community repository (`19.0`).
- Is discovered through `addons_path`; it is not run directly.

### `odoo-trainning-dev`

- Git repository for custom addon development.
- Currently contains the `dealer_financing` application.
- Custom code should be committed here rather than in the Community or
  Enterprise repositories.

## Dealer Financing Module

```text
dealer_financing/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── loan_application.py
│   ├── loan_application_document.py
│   ├── loan_application_document_type.py
│   └── loan_application_tag.py
├── security/
│   ├── dealer_financing_groups.xml
│   ├── dealer_financing_security.xml
│   └── ir.model.access.csv
├── views/
│   ├── dealer_financing_menu.xml
│   ├── loan_application_document_type_views.xml
│   ├── loan_application_tag_views.xml
│   └── loan_application_views.xml
└── demo/
    ├── config_demo.xml
    └── loan_demo.xml
```

### Root Files

- `__init__.py` imports the module's Python packages.
- `__manifest__.py` defines module metadata, dependencies, data-file loading
  order, demo data, licensing, and application status.
- The module currently depends on the standard `product` addon.

### Models

| Python file | Odoo model | Purpose |
| --- | --- | --- |
| `loan_application.py` | `loan.application` | Main loan application, customer, motorcycle, financing values, status, tags, documents, and notes. |
| `loan_application_document.py` | `loan.application.document` | Document checklist entry attached to a loan application. |
| `loan_application_document_type.py` | `loan.application.document.type` | Configurable document types and required-document flags. |
| `loan_application_tag.py` | `loan.application.tag` | Reusable, color-coded application tags. |

The main relationships are:

```text
res.partner ───────────────┐
product.template ──────────┤
res.users ─────────────────┤
loan.application.tag ──────┤ many-to-many
                           ▼
                    loan.application
                           │ one-to-many
                           ▼
              loan.application.document
                           │ many-to-one
                           ▼
           loan.application.document.type
```

### Security

`dealer_financing_groups.xml` defines the Dealership category, Financing
privilege, and two roles:

- **User** implies the standard internal-user group.
- **Admin** implies the Dealer Financing User group.

`ir.model.access.csv` defines model-level permissions:

| Model | User | Admin |
| --- | --- | --- |
| Loan Applications | Full access | Full access |
| Tags | Read-only | Full access |
| Document Types | Read-only | Full access |
| Loan Documents | Full access | Full access |

`dealer_financing_security.xml` defines record rules for loan applications:

- Users cannot write or delete signed applications.
- Admins can write and delete applications in every state.
- Read and create operations are governed by model access because these rules
  are disabled for those operations.

### Views and Navigation

- `loan_application_views.xml` provides list, form, and search interfaces for
  loan applications. Documents are managed from the Compliance Checklist tab.
- `loan_application_tag_views.xml` provides tag list and form actions.
- `loan_application_document_type_views.xml` provides document-type list and
  form actions.
- `dealer_financing_menu.xml` builds the Financing application menu. The
  configuration menus are visible only to Dealer Financing Admins.

### Demo Data

- `config_demo.xml` creates example tags and required document types.
- `loan_demo.xml` creates sample loan applications.
- Demo records load only when the database is created or the module is
  installed with demo data enabled.

## Module Data Loading Order

Odoo loads the files listed in `__manifest__.py` in this order:

1. Groups and privileges.
2. Model access controls.
3. Record rules.
4. Loan application views.
5. Tag views.
6. Document type views.
7. Menus and actions.

This order ensures that groups exist before access controls reference them and
that actions exist before menus reference those actions.

## Common Development Commands

Run commands from the Community repository:

```bash
cd /home/shikhar_gc/odoo
```

Start the server:

```bash
./venv/bin/python odoo-bin -c odoo.conf
```

Install the custom module in a database:

```bash
./venv/bin/python odoo-bin -c odoo.conf \
  -d DATABASE_NAME \
  -i dealer_financing \
  --stop-after-init
```

Upgrade the module after Python, XML, CSV, or manifest changes:

```bash
./venv/bin/python odoo-bin -c odoo.conf \
  -d DATABASE_NAME \
  -u dealer_financing \
  --stop-after-init
```

Install the Enterprise web interface:

```bash
./venv/bin/python odoo-bin -c odoo.conf \
  -d DATABASE_NAME \
  -i web_enterprise \
  --stop-after-init
```

Replace `DATABASE_NAME` with the target PostgreSQL database name. Restart the
normal server process after a stop-after-init command completes.

## Development Guidelines

- Keep Community and Enterprise checked out on the same Odoo version branch.
- Put custom modules in `odoo-trainning-dev`.
- Import each new Python model from `models/__init__.py`.
- Declare every XML or CSV data file in `__manifest__.py` in dependency order.
- Add model-level access for every new persistent model.
- Upgrade the module after changing fields, views, security, or data files.
- Test security using both Dealer Financing User and Admin accounts.
- Do not commit database passwords, subscription codes, generated bytecode, or
  local runtime data.
