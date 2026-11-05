# Patent reading notes — GB2591502A

**Source:** [GB2591502A, Hair applicator](https://patents.google.com/patent/GB2591502A/en)  
**Additional figure copy inspected:** [EP4096470B1, official EPO publication PDF](https://data.epo.org/publication-server/rest/v1.2/publication-dates/2024-08-21/patents/EP4096470NWB1/document.pdf)  
**Use in this project:** technical disclosure reference only; not a manufacturing specification, product teardown or freedom-to-operate opinion.

## Bibliographic metadata (Google Patents transcription)

- Publication: GB2591502A
- Inventor field: Mouhamad Youmna
- Assignee fields: Myana Naturals Ltd (current/original assignee shown by Google Patents; verify against the official register)
- Priority / filing date shown: 31 January 2020
- Publication date shown: 4 August 2021
- Grant event shown: 13 April 2022
- Google Patents page currently labels the status “Expired - Fee Related”. Google explicitly cautions that legal status and assignee data may be inaccurate and are not legal conclusions. Verify status, proprietor, events and family in the official UK IPO register before relying on them.

## Relationship to the Nyfasi brand and retail product

The patent metadata identifies Mouhamad Youmna and Myana Naturals Ltd. The Royal Academy of Engineering identifies Dr Youmna Mouhamad as Nyfasi's founder and CEO and describes the Deluxe Detangler as Nyfasi's patented technology; Le Journal de Mayotte also calls the Deluxe Detangler Nyfasi's patented innovation. Combined with the inventor/assignee and family metadata, this is strong cross-source evidence that the family relates to Nyfasi's product. However, neither institutional nor media source explicitly maps publication number GB2591502A to a specific retail SKU or revision. The exact publication-to-retail-revision mapping therefore remains unverified pending primary confirmation.

## Disclosed architecture

The abstract and description disclose a hair comb/applicator comprising:

1. A body enclosing a reservoir for hair-treatment substance.
2. A row or rows of teeth.
3. A roller mounted rotatably in the body to transfer treatment substance from the reservoir to hair.
4. A wall with a concave inner surface seating the roller and a convex outer surface carrying the teeth.
5. Through-slots between teeth, each extending as an arc along the wall.
6. A body that may be formed from inter-engageable upper and lower housing portions.
7. A roller drum with textured bands/projections aligned to slots and smoother intervening sealing surfaces.
8. Spindle pins at roller ends, retained by corresponding recesses/arms in the housing.
9. A resilient seal and snap-fit housing interface in described embodiments.

The description says the illustrated embodiment has eight teeth, approximately 5 mm wide, with adjacent spacing of approximately 10 mm. It describes the teeth as blade-shaped and tapered. The text further says the tooth length is approximately twice the tooth width. These are disclosed embodiment details, not proof that every retail unit or later product revision has those exact features.

## Figure-based geometry interpretation

The official EPO publication PDF was inspected directly:

- **Figure 5 (PDF page 13):** transverse section showing the concave inner seat (64), convex exterior wall (61), roller (30), through-slots (62), and blade teeth (40).
- **Figure 6A (PDF page 14):** schematic cross-section of a cylindrical wall segment with an obtuse central angle greater than 90 degrees.
- **Figure 6B (PDF page 14):** semi-cylindrical wall segment with an approximately 180-degree central angle. The description explains that increasing this angle increases the wall/slot arc length and that angles greater than 180 degrees can overhang the roller.
- **Figure 3 (PDF page 12):** roller drum with circumferential textured bands (34), smooth sealing lands (36), end walls (31) and spindle pins (32).
- **Figures 1–4 (PDF pages 10–12):** exploded assembly, exterior views, roller and longitudinal section.

The current model uses the Figure 6B 180-degree embodiment as a practical construction target. This is a patent-led interpretation, not a measured retail value. It models one slot in each of the seven gaps between eight teeth. That slot count is an engineering interpretation of “interposed between” and is not stated as a dimensioned count in the drawing.

See [curved-wall geometry reconstruction](curved-wall-geometry.md) for the parameter ledger, coordinate convention and limitations.

## What this changes in the reconstruction

The model now represents a 180-degree annular wall segment with a concave roller seat and seven axial-band cuts that appear as circumferential arcs in cross-section. The roller axis and tooth row share a longitudinal axis. The teeth remain simplified rectangular blades; taper and elliptical cross-section are not yet modelled.

## Interpretation limits

- A patent disclosure describes claimed subject matter and embodiments; it is not necessarily the exact product sold under the Nyfasi brand.
- The Google Patents status display is not an official legal-status opinion.
- The patent text and figures are not native CAD or a production drawing package.
- Patent publication does not establish permission to reproduce protected images or commercialise a reconstruction.
- The curved wall and slot geometry has not been validated against an authorised physical sample or dimensioned manufacturing drawing.
- The Sand3D workflow has previously produced structurally readable GLB/OBJ files for the earlier flat proxy. The new curved-wall iteration must pass the same build workflow before its exports can be described as generated.

## China family member and international record

The related Chinese family member is [CN115003190B](https://patents.google.com/patent/CN115003190B/en), application CN202180011338.5, with application publication CN115003190A dated 2 September 2022 and B publication/grant event dated 9 April 2024. The shared priority date is 31 January 2020. The [US family record](https://patents.google.com/patent/US20230088345A1/en) lists the Chinese member and the family publication dates.

Google Patents' family view labels the Chinese member active, but that is not a formal CNIPA legal-status certificate. The official verification route is the [CNIPA patent search portal](https://cponline.cnipa.gov.cn/). This project has not yet captured an official CNIPA register extract or verified current fee/payment history and chain of title.

The UK, Chinese, European and US publications belong to the same disclosed applicator family, but national claims and legal events must be checked separately. Do not assume the same claim scope or enforceability applies in every territory.
