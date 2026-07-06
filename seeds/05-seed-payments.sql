-- ===========================================================================================================
-- SEED DATA: Payment Methods & Disbursement Configs
-- Run AFTER the main db.sql migration and after insurance_companies + banks are populated
-- ===========================================================================================================

-- PAYMENT METHODS
-- MoMo and Bank for ALL insurers
INSERT INTO payment_methods (insurance_company_id, method, enabled)
SELECT ic.id, 'momo', true
FROM insurance_companies ic
WHERE ic.deleted = false
ON CONFLICT DO NOTHING;

INSERT INTO payment_methods (insurance_company_id, method, enabled)
SELECT ic.id, 'bank', true
FROM insurance_companies ic
WHERE ic.deleted = false
ON CONFLICT DO NOTHING;

-- Pay-small-small ONLY for Millennium Insurance.
-- Matches both "Millennium" (prod) and the legacy "Milinium" spelling (local seeds)
-- so this seed works against either environment.
INSERT INTO payment_methods (insurance_company_id, method, enabled)
SELECT ic.id, 'pay-small-small', true
FROM insurance_companies ic
WHERE (ic.name ILIKE '%millennium%' OR ic.name ILIKE '%milinium%')
  AND ic.deleted = false
ON CONFLICT DO NOTHING;


-- ===========================================================================================================
-- DISBURSEMENT CONFIGS
-- Full payment -> insurer's own bank account (from insurer_banks)
-- Note: pay-small-small is intentionally NOT seeded into disbursement_configs.
-- Hubtel + Albrim disburse PSS premiums to the insurer directly; MyPolicy never
-- holds those funds and the backend skips the disbursement check / transfer job
-- when paymentMethod === 'pay-small-small'.
-- ===========================================================================================================

-- For each insurer, create a 'full' disbursement config pointing to their bank
INSERT INTO disbursement_configs (insurance_company_id, payment_method, target_name, bank_id, bank_account_number, bank_account_name, bank_branch)
SELECT
    ib.insurance_company_id,
    'full',
    ic.name,
    ib.bank_id,
    ib.account_number,
    ic.name,
    ib.branch
FROM insurer_banks ib
JOIN insurance_companies ic ON ib.insurance_company_id = ic.id
WHERE ib.deleted = false AND ic.deleted = false
ON CONFLICT DO NOTHING;
