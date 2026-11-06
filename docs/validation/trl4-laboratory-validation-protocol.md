# TRL 4 laboratory validation protocol

**Technology under test:** Product Engineering Lab / Sand3D Nyfasi research proxy  
**Current evidence status:** provisional TRL 3; TRL 4 not yet demonstrated.

## 1. Validation boundary

The assessed technology is the evidence-linked parameter ledger, procedural assembly generator, constraint checks, parametric edit benchmark and interoperable exports. The current Nyfasi geometry is a research proxy. Patent-derived values, image estimates and engineering assumptions are not physical measurements.

This campaign does not establish retail-product identity, manufacturing readiness, safety, regulatory compliance, material performance, durability or fitness for use.

## 2. Entry criteria

Before a laboratory test is marked executed:

1. Freeze the source commit, dependency versions, parameter-ledger hash and procedure revision.
2. Identify the physical reference article and record provenance, revision and permission to measure. Without an authorised sample or authoritative controlled drawing, dimensional correlation is BLOCKED.
3. Establish a datum scheme and identify each measured feature.
4. Record instrument make/model, serial number, calibration status, due date, resolution and measurement uncertainty.
5. Approve the measurement plan and acceptance criteria before collecting results. Criteria must come from a traceable specification or a documented research requirement, not be selected after seeing results.
6. Record operator, date/time, environmental conditions and laboratory location.

## 3. Test campaign

| ID | Test | Method | Evidence |
|---|---|---|---|
| L01 | Build reproducibility | Rebuild the frozen commit in three clean workspaces | Run IDs, environment, logs, hashes, exit codes |
| L02 | Parametric sensitivity | Baseline, roller +2 mm and housing +10 mm cases | Benchmark JSON, export hashes and measured bounds |
| L03 | Invalid-input rejection | Submit roller diameter below the declared geometric minimum | Rejection log proving build was not invoked |
| L04 | Dimensional correlation | Measure agreed physical features using calibrated instruments and frozen datums | Raw readings, certificates, uncertainty budget, deviations |
| L05 | Interface/clearance assessment | Measure roller/seat, band/slot and spindle/bearing interfaces where accessible | Raw readings, min/max clearance, uncertainty, photographs |
| L06 | Independent review | Second competent reviewer checks protocol, raw data, calculations and traceability | Signed review and disposition |

L01–L03 are software/workflow checks. L04–L06 require real physical evidence. A software-only pass must never be represented as physical validation.

## 4. Measurement method and uncertainty

For each physical feature, record at least three repeat readings at each defined location, instrument resolution, calibration status, operator and conditions. Add positions where geometry, runout or local variation makes a single point unrepresentative.

Report individual readings, mean, range, instrument uncertainty and a documented combined uncertainty. Do not silently discard outliers. Compare CAD and physical results using pre-approved criteria and the uncertainty interval.

Dimensional inspection alone does not establish material properties, seal compression, fatigue life, wear, contact mechanics or dynamic performance.

## 5. Acceptance and decision rules

- Software tests must pass on the frozen commit and the evidence bundle must be retained.
- Physical comparisons pass only against pre-approved, traceable criteria with uncertainty accounted for.
- Missing sample, uncalibrated instrument, unknown datum, unapproved criterion or missing raw data means BLOCKED, not PASS.
- Preserve failures and deviations; never overwrite a failed run with a later passing run.
- TRL 4 may be considered only after validation in a controlled laboratory environment with reproducibility, traceability and independent review. A green CI badge alone is insufficient.

## 6. Evidence package

Retain source commit and parameter hash; dependency/environment record; CI URLs and logs; benchmark JSON; generated GLB/OBJ/URDF/USD outputs and SHA-256 hashes; raw measurement sheets; calibration certificates; uncertainty calculations; photographs; deviations; and independent reviewer sign-off.

The machine-readable evidence register deliberately starts with physical validation NOT_STARTED. Update it only from actual test records.

## 7. Current known limitations

The CAD parameter ledger contains engineering assumptions and image estimates. The tolerance ledger describes assumed inputs. No authorised, calibrated physical reference dataset is currently evidenced. The repository can improve software verification now, but L04–L06 depend on access to a suitable sample or controlled drawings and calibrated metrology.

**Status conclusion:** this protocol prepares a TRL 4 laboratory campaign; it is not evidence that the campaign has been completed.
