# Licensing status

**Status: undecided. No project-wide open-source licence is currently granted.**

The repository previously contained an MIT licence file. It has been removed because the project owner has not selected a public licence. Public availability on GitHub is not, by itself, an open-source licence. Unless a file has a separate explicit licence, original repository material remains subject to its author's rights and applicable default copyright law.

This repository grants no rights to Nyfasi product designs, patent claims, trademarks, photographs, product copy, PDR/iF Design materials or other third-party work. Sand3D is a separate project distributed under Apache License 2.0; that licence applies to Sand3D, not this repository. Follow Sand3D's own licence and notices when using or redistributing it.

## Intended hybrid direction (not a licence grant)

1. **Potential public layer:** reusable evidence schemas, provenance conventions, evaluation fixtures and non-sensitive adapters, after ownership review.
2. **Potential commercial layer:** proprietary AK Build orchestration, private integrations, validation workflows, managed services and customer-specific engineering pipelines, licensed by contract.
3. **Third-party layer:** Nyfasi, patent, PDR, iF Design, Sand3D and dataset materials remain governed by their respective owners' rights and licences.

## Licence options to evaluate

| Licence | What it permits / requires | Fit for this project |
|---|---|---|
| **Apache-2.0** | Permissive reuse, including commercial forks; includes an express patent licence and requires preservation of notices | Strong candidate for stable public schemas, SDKs, adapters and evaluation tools. It does not stop a competitor selling a fork |
| **MIT** | Very short permissive licence; commercial reuse and forks allowed; no equivalent express patent grant in the licence text | Simple, but less attractive than Apache-2.0 for patent-sensitive engineering tooling |
| **MPL-2.0** | File-level weak copyleft: modifications to MPL-covered files stay under MPL; larger combined works may contain proprietary files | Useful if you want improvements to selected public files to remain shared without forcing the whole platform open |
| **AGPL-3.0** | Strong copyleft, including source-offer obligations for modified versions used over a network | Consider only if reciprocal sharing of network-deployed modifications is a deliberate requirement; may complicate enterprise adoption |
| **BSL-1.1** | Source-available under a custom additional-use grant and change date; not an OSI-approved open-source licence | Consider for a source-visible proprietary core if commercial restrictions are essential; requires careful, project-specific drafting |
| **Proprietary contract** | Use, access, support, hosting and deliverable rights defined by agreement | Appropriate for AK Build enterprise modules, private integrations, managed validation and customer-specific work |

Official texts: [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0), [MIT](https://opensource.org/license/mit), [MPL-2.0](https://www.mozilla.org/en-US/MPL/2.0/), [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.en.html), [BSL-1.1](https://mariadb.com/bsl11/).

## Working recommendation for the hybrid model

If the ownership audit supports it, a practical default to evaluate is:

- **Apache-2.0:** public schemas, provenance format, reference adapters, command-line utilities and reproducible evaluation fixtures.
- **Proprietary:** AK Build orchestration, hosted control plane, private integrations, customer-specific connectors, enterprise policy packs and managed workflows.
- **Services:** paid discovery, evidence modelling, reconstruction R&D, validation, implementation, training and support.
- **Third-party materials:** remain under their own terms; do not bundle them into an open layer without permission.

This creates a route to adoption without pretending that an Apache-licensed schema itself prevents competitors from commercialising it. Commercial value must come from execution, integrations, operational assurance, support, hosting, customer-specific work and separately licensed modules.

## Before changing this status

- Confirm copyright ownership and employment, university, client, contractor and contributor obligations.
- Audit every file, dependency, model, dataset, image and generated artefact.
- Record third-party licence notices and attribution requirements.
- Decide exactly which directories and file classes belong to the public layer.
- Consider a Developer Certificate of Origin or Contributor Licence Agreement before accepting contributions intended for dual licensing.
- Add the selected licence file, SPDX identifiers and required notices only after approval.
- Review the commercial agreement so background IP, foreground deliverables, third-party IP and customer data are distinguished.

This is a project governance note, not legal advice. Obtain qualified IP advice before licensing, manufacturing, distributing or commercially using a reconstruction.

## Further reading

- [UK IPO: licensing intellectual property](https://www.gov.uk/guidance/licensing-intellectual-property)
- [UK IPO: licensing copyright](https://www.gov.uk/guidance/license-sell-or-market-your-copyright-material)
- [Business.gov.uk: managing IP when working with others](https://www.business.gov.uk/support/intellectual-property/managing-intellectual-property-working-with-others/)
- [Sand3D repository and licence](https://github.com/Sandflow-ai/sand3d)
