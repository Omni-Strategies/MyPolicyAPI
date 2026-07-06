-- ===========================================================================================================
-- SEED DATA — MyPolicy / Althia
-- (countries, banks, insurance_companies, and payments are seeded separately — not included here)
-- ===========================================================================================================

-- ADMINS
INSERT INTO admins (id, first_name, last_name, email, phone, department, password, status) VALUES
('20000000-0000-0000-0000-000000000001', 'Ama', 'Mensah', 'ama.mensah@mypolicy.com', '0244000001', 'Operations', '$2b$10$examplehash1', 'active'),
('20000000-0000-0000-0000-000000000002', 'Kofi', 'Owusu', 'kofi.owusu@mypolicy.com', '0244000002', 'Underwriting', '$2b$10$examplehash2', 'active');

-- AGENCIES
INSERT INTO agencies (id, name, logo, created_by) VALUES
('30000000-0000-0000-0000-000000000001', 'Accra Insurance Brokers', '/images/agencies/accra-brokers.png', '20000000-0000-0000-0000-000000000001'),
('30000000-0000-0000-0000-000000000002', 'Tema Risk Partners', '/images/agencies/tema-risk.png', '20000000-0000-0000-0000-000000000001');

-- ROLES
INSERT INTO roles (id, name, role_type, organization_id) VALUES
('40000000-0000-0000-0000-000000000001', 'Super Admin', 'admin', NULL),
('40000000-0000-0000-0000-000000000002', 'Agent', 'agent', '30000000-0000-0000-0000-000000000001'),
('40000000-0000-0000-0000-000000000003', 'Customer', 'customer', NULL);

-- PERMISSIONS
INSERT INTO permissions (id, name, action, module, role_id, organization_id) VALUES
('41000000-0000-0000-0000-000000000001', 'Manage Policies', 'write', 'policies', '40000000-0000-0000-0000-000000000001', NULL),
('41000000-0000-0000-0000-000000000002', 'View Quotes', 'read', 'quotes', '40000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000001');

-- VEHICLE MAKES
INSERT INTO vehicle_makes (id, name, created_by) VALUES
('50000000-0000-0000-0000-000000000001', 'Toyota', '20000000-0000-0000-0000-000000000001'),
('50000000-0000-0000-0000-000000000002', 'Honda', '20000000-0000-0000-0000-000000000001');

-- VEHICLE MODELS
INSERT INTO vehicle_models (id, name, make_id, created_by) VALUES
('51000000-0000-0000-0000-000000000001', 'Corolla', '50000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001'),
('51000000-0000-0000-0000-000000000002', 'Camry', '50000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001'),
('51000000-0000-0000-0000-000000000003', 'Civic', '50000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000001'),
('51000000-0000-0000-0000-000000000004', 'Accord', '50000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000001');

-- BUSINESS ENTITIES
INSERT INTO business_entities (id, name, logo, tin_no, created_by) VALUES
('70000000-0000-0000-0000-000000000001', 'Kwame Logistics Ltd', '/images/entities/kwame-logistics.png', 'TIN-0001', '20000000-0000-0000-0000-000000000001');

-- AGENTS
INSERT INTO agents (id, first_name, last_name, email, agent_code, phone, country_id, digital_address, physical_address, postal_address, password, status, created_by, organization_id) VALUES
('80000000-0000-0000-0000-000000000001', 'Esi', 'Asante', 'esi.asante@accrabrokers.com', 'AGT-001', '0201000001', (SELECT id FROM countries WHERE name = 'Ghana' LIMIT 1), 'GA-123-4567', '12 Ring Road, Accra', 'PO Box 100, Accra', '$2b$10$examplehash3', 'active', '20000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001'),
('80000000-0000-0000-0000-000000000002', 'Yaw', 'Boateng', 'yaw.boateng@temarisk.com', 'AGT-002', '0201000002', (SELECT id FROM countries WHERE name = 'Ghana' LIMIT 1), 'GT-456-7890', '5 Harbour Road, Tema', 'PO Box 200, Tema', '$2b$10$examplehash4', 'active', '20000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000002');

-- CUSTOMERS
INSERT INTO customers (id, first_name, last_name, email, digital_address, gender, customer_type, gh_card_no, country_id, dob, phone, password, created_by, business_entity_id) VALUES
('90000000-0000-0000-0000-000000000001', 'Abena', 'Osei', 'abena.osei@gmail.com', 'GA-111-2222', 'female', 'individual', 'GHA-000111222-1', (SELECT id FROM countries WHERE name = 'Ghana' LIMIT 1), '1990-05-14', '0244111222', '$2b$10$examplehash5', '20000000-0000-0000-0000-000000000001', NULL),
('90000000-0000-0000-0000-000000000002', 'Kwesi', 'Appiah', 'kwesi.appiah@gmail.com', 'GT-333-4444', 'male', 'individual', 'GHA-000333444-1', (SELECT id FROM countries WHERE name = 'Ghana' LIMIT 1), '1985-11-02', '0244333444', '$2b$10$examplehash6', '20000000-0000-0000-0000-000000000001', NULL),
('90000000-0000-0000-0000-000000000003', 'Adjoa', 'Frimpong', 'adjoa.frimpong@kwamelogistics.com', 'GA-555-6666', 'female', 'business', 'GHA-000555666-1', (SELECT id FROM countries WHERE name = 'Ghana' LIMIT 1), '1992-03-21', '0244555666', '$2b$10$examplehash7', '20000000-0000-0000-0000-000000000001', '70000000-0000-0000-0000-000000000001');

-- INSURANCE PRODUCTS
INSERT INTO insurance_products (id, name, image, created_by) VALUES
('b0000000-0000-0000-0000-000000000001', 'Motor Comprehensive', '/images/products/motor-comprehensive.png', '20000000-0000-0000-0000-000000000001'),
('b0000000-0000-0000-0000-000000000002', 'Motor Third Party', '/images/products/motor-third-party.png', '20000000-0000-0000-0000-000000000001'),
('b0000000-0000-0000-0000-000000000003', 'Fire Insurance', '/images/products/fire.png', '20000000-0000-0000-0000-000000000001');

-- COMMISSIONS (agent/agency level)
INSERT INTO commissions (id, rate, agent_id, agency_id, cover_type, insurance_product_id, created_by) VALUES
('c0000000-0000-0000-0000-000000000001', 0.10, '80000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001', 'comprehensive', 'b0000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001'),
('c0000000-0000-0000-0000-000000000002', 0.07, '80000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000002', 'third_party', 'b0000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000001');

-- INSURANCE COMMISSIONS (company level)
INSERT INTO insurance_commissions (id, agency_rate, agent_rate, cover_type, insurance_product_id, insurance_company_id, created_by) VALUES
('c1000000-0000-0000-0000-000000000001', 0.15, 0.10, 'comprehensive', 'b0000000-0000-0000-0000-000000000001', (SELECT id FROM insurance_companies ORDER BY created_at LIMIT 1 OFFSET 0), '20000000-0000-0000-0000-000000000001'),
('c1000000-0000-0000-0000-000000000002', 0.12, 0.07, 'third_party', 'b0000000-0000-0000-0000-000000000002', (SELECT id FROM insurance_companies ORDER BY created_at LIMIT 1 OFFSET 1), '20000000-0000-0000-0000-000000000001');

-- SYSTEM COMMISSIONS
INSERT INTO system_commissions (id, rate, created_by) VALUES
('c2000000-0000-0000-0000-000000000001', 0.02, '20000000-0000-0000-0000-000000000001');

-- INSURANCE REQUESTS
INSERT INTO insurance_requests (id, insurance_product_id, registered_no, request_data, requested_by, intermediary_id, assigned_agent_id, assigned_agency_id, status, responded_by) VALUES
('e0000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000001', 'GT-1234-24', '{"vehicle":"Toyota Corolla","year":2020}', '90000000-0000-0000-0000-000000000001', '80000000-0000-0000-0000-000000000001', '80000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001', 'responded', '80000000-0000-0000-0000-000000000001'),
('e0000000-0000-0000-0000-000000000002', 'b0000000-0000-0000-0000-000000000002', 'GT-5678-24', '{"vehicle":"Honda Civic","year":2019}', '90000000-0000-0000-0000-000000000002', '80000000-0000-0000-0000-000000000002', '80000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000002', 'pending', NULL);

-- QUOTES
INSERT INTO quotes (id, insurance_company_id, insurance_request_id, info, premium, agent_commission, created_by, status, responded_by) VALUES
('f0000000-0000-0000-0000-000000000001', (SELECT id FROM insurance_companies ORDER BY created_at LIMIT 1 OFFSET 0), 'e0000000-0000-0000-0000-000000000001', 'Comprehensive cover, 12 months', 1500.00, 150.00, '80000000-0000-0000-0000-000000000001', 'accepted', '90000000-0000-0000-0000-000000000001');

-- POLICIES
INSERT INTO policies (id, quote_id, insurance_company_id, insurance_request_id, start_date, end_date, created_by, status) VALUES
('01000000-0000-0000-0000-000000000001', 'f0000000-0000-0000-0000-000000000001', (SELECT id FROM insurance_companies ORDER BY created_at LIMIT 1 OFFSET 0), 'e0000000-0000-0000-0000-000000000001', '2026-01-01', '2026-12-31', '90000000-0000-0000-0000-000000000001', 'active');

-- FORM REQUESTS
INSERT INTO form_requests (id, insurance_product_id, request_data, requested_by, status, responded_by) VALUES
('02000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000003', '{"property":"Warehouse","location":"Tema"}', '90000000-0000-0000-0000-000000000003', 'pending', NULL);

-- POLICY DOCUMENTS
INSERT INTO policy_documents (id, document_key, description, policy_id, created_by, created_for) VALUES
('03000000-0000-0000-0000-000000000001', 'policies/01000000/schedule.pdf', 'Policy schedule', '01000000-0000-0000-0000-000000000001', '80000000-0000-0000-0000-000000000001', '90000000-0000-0000-0000-000000000001');

-- PAYMENT METHODS
INSERT INTO payment_methods (id, insurance_company_id, method, enabled, created_by) VALUES
('07000000-0000-0000-0000-000000000001', (SELECT id FROM insurance_companies ORDER BY created_at LIMIT 1 OFFSET 0), 'mobile_money', true, '20000000-0000-0000-0000-000000000001'),
('07000000-0000-0000-0000-000000000002', (SELECT id FROM insurance_companies ORDER BY created_at LIMIT 1 OFFSET 1), 'card', true, '20000000-0000-0000-0000-000000000001');