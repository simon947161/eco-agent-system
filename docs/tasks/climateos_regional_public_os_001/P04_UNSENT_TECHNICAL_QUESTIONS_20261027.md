# Provider clarification questions — UNSENT

Prepared2026-10-27 for owner review. No external enquiry sent; no Council representation.

For Bureau AWRA product support (native historical/v1/AWRALv7/processed/values/month/rain_day.nc and sm_pct.nc):

1. Does monthly rain_day represent the sum of daily rainfall, a daily mean, or another statistic? Does monthly sm_pct represent a time mean or month-end state? Please identify the processing version and missing/partial-month policy; neither native variable has cell_methods.
2. sm_pct declares fraction of fullness with no scale_factor/add_offset or valid_range. What stored range and physical reference define fullness? Is percentage conversion only a presentation operation?
3. The sampled monthly bounds run from first-of-month to next first-of-month, with a month-end label. What are the underlying daily rainfall/model-day interval, time zone and DST rules? Are bounds merely calendar labels or physical instants?
4. How should consumers identify a reproducible data revision when native date_modified remains2021 but HTTP Last-Modified is2026? What masks/QC/completeness information accompanies the monthly product?

For Bureau HRS/WaterNSW data-product support (410033, September2026 public HRS release):

1. Does9am local mean fixed standard time or civil time with DST? How are23/25-hour transition days handled alongside the header's previous24hours wording?
2. Does the CSV date denote interval end or start, and how are cross-month intervals assigned to the official monthly totals? Please specify calendar-month versus water-year handling.
3. Is the cubic-metres extraction converted to ML before publication, and where is the transformation documented?
4. Why does the February monthly CSV stop at2025 although the daily release covers February2026, while both show September2026 and extraction date4/06/2024? Are the monthly products synchronized to the daily release?
5. How are E/C/G records and missing values represented in monthly totals without a quality column? Can a monthly quality/completeness summary be obtained?

Acceptance after clarification: retain exact reply/document version and hash, update the result matrix, and only then run a narrow independently reviewable month reconciliation. No numeric join or correlation is authorized by the existence of these questions.
