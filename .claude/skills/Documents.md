# Documents Module Standards

## Purpose

The `documents/` directory stores personal reference documents — bills, leases, invoices, insurance policies, identity docs, and employment contracts. It is separate from `personal_finance/` (data pipeline) and `taxes/` (filing/compliance).

## Directory Structure

```
documents/
  lease/          # Lease agreements (rental, vehicle, etc.)
  bills/          # Utility bills, subscriptions, service charges
  invoices/       # Invoices sent or received
  insurance/      # Policies, claim documents, coverage letters
  identity/       # Passport scans, IDs, citizenship docs
  employment/     # Employment agreements, offer letters, termination letters
```

Each subdirectory (except `identity/`) is organized by year:

```
documents/bills/2026/
documents/lease/2024/
```

`identity/` is flat — these documents don't naturally group by year.

## File Naming Convention

```
YYYY-MM-DD_vendor_description.ext
```

| Field | Format | Required | Notes |
|---|---|---|---|
| Date | `YYYY-MM-DD` or `YYYY-MM` | Yes | Day is optional when no specific day applies |
| Vendor | lowercase, hyphenated | Yes | Source/issuer of the document |
| Description | lowercase, hyphenated | Yes | What the document is |
| Separator | `_` between fields, `-` within fields | — | Underscores delimit fields; hyphens delimit words |

### Examples

```
2026-03-01_enmax_electricity-bill.pdf
2025-08_helios_employment-agreement.pdf
2024-10_blvd-beltline_lease.pdf
2024-08-20_cms_moving-deposit-receipt.pdf
2025-01_sun-life_health-policy.pdf
passport_scan.pdf                          # identity/ — no date prefix needed
drivers-license_scan.pdf                   # identity/ — no date prefix needed
```

## Boundary Rules

| Goes in `documents/` | Goes in `personal_finance/` | Goes in `taxes/` |
|---|---|---|
| Signed agreements, leases | Transaction CSVs & statement PDFs | Tax slips (T4, T5, etc.) |
| Utility/service bills | SQLite DB, dbt models, scripts | Returns & NOAs |
| Invoices sent/received | Budget reports | CRA disputes & correspondence |
| Insurance policies | | |
| Identity docs | | |
| Employment contracts | | |

## Rules

- New subdirectories can be added freely if a new document category emerges.
- Year directories are created as needed — don't pre-create empty year folders.
- All filenames must follow the naming convention above for consistency and sortability.
- A document belongs here if it's a **reference record** you might need to look up later, not analytical source data or tax compliance material.
