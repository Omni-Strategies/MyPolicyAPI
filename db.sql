CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TYPE gender_enum AS ENUM ('male', 'female');


-- ===========================================================================================================

CREATE TABLE IF NOT EXISTS admins(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	first_name varchar(150) not null,
	last_name varchar(150) not null,
    email varchar, 
    image varchar, 
    department varchar, 
    status varchar default 'active', 
    phone varchar(16) not null,
    password varchar,
    roles uuid[],
    created_by uuid,
    deleted boolean default false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ===========================================================================================================

CREATE TABLE IF NOT EXISTS vehicle_makes(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	name varchar(150) not null,
    models jsonb[],
    created_by uuid,
    deleted boolean default false,
    CONSTRAINT FK_admin FOREIGN KEY(created_by) REFERENCES admins(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE IF NOT EXISTS vehicle_models(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	name varchar(150) not null,
    make_id uuid,
    created_by uuid,
    deleted boolean default false,
    CONSTRAINT FK_make FOREIGN KEY(make_id) REFERENCES vehicle_makes(id),
    CONSTRAINT FK_admin FOREIGN KEY(created_by) REFERENCES admins(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



-- ===========================================================================================================

CREATE TABLE IF NOT EXISTS banks(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	name varchar(150) not null,
    bank_code varchar NOT NULL,
    created_by uuid,
    deleted boolean default false,
    CONSTRAINT FK_admin FOREIGN KEY(created_by) REFERENCES admins(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



-- ===========================================================================================================

CREATE TABLE IF NOT EXISTS countries(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	name varchar(150) not null,
    code varchar,
    deleted boolean default false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agencies(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	name varchar(150) not null,
	logo varchar not null,
    created_by uuid,
    deleted boolean default false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================================================================================

CREATE TABLE IF NOT EXISTS roles(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	name varchar(150) not null,
    role_type varchar,
    deleted boolean default false,
    organization_id uuid,
    CONSTRAINT FK_organization FOREIGN KEY(organization_id) REFERENCES agencies(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	name varchar(150) not null,
    action varchar not null,
    module varchar not null,
    deleted boolean default false,
    role_id uuid,
    organization_id uuid,
    CONSTRAINT FK_organization FOREIGN KEY(organization_id) REFERENCES agencies(id),
    CONSTRAINT FK_role FOREIGN KEY(role_id) REFERENCES roles(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================================================================================



CREATE TABLE IF NOT EXISTS agents(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	first_name varchar(150) not null,
	last_name varchar(150) not null,
    email varchar, 
	intermediary_id uuid,
    intermediary_type varchar default 'agent',
    agent_code varchar,
    phone varchar(16) not null,
    image varchar,
    nic_document varchar,
    agreement_document varchar,
    country_id uuid,
    digital_address varchar not null,
    physical_address varchar not null,
    postal_address varchar not null,
    password varchar,
    roles uuid[],
    deleted boolean default false,
    status varchar not null default 'active',
    created_by uuid,
    organization_id uuid,
    CONSTRAINT FK_organization FOREIGN KEY(organization_id) REFERENCES agencies(id),
    CONSTRAINT FK_country FOREIGN KEY(country_id) REFERENCES countries(id),
    CONSTRAINT FK_admin FOREIGN KEY(created_by) REFERENCES admins(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS agent_requests(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
    request_type varchar not null,
    request_data jsonb not null,
    deleted boolean default false,
    status varchar default 'pending',
    reason varchar,
    approved_by uuid,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ===========================================================================================================


CREATE TABLE IF NOT EXISTS business_entities(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	name varchar(150) not null,
	logo varchar not null,
	tin_no varchar not null,
    deleted boolean default false,
    created_by uuid,
    CONSTRAINT FK_admin FOREIGN KEY(created_by) REFERENCES admins(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	first_name varchar(150) not null,
	last_name varchar(150) not null,
    email varchar, 
    digital_address varchar, 
    gender gender_enum default 'male',
    customer_type varchar, 
    gh_card_no varchar, 
    country_id uuid,
    dob varchar,
    phone varchar(16) not null,
    password varchar,
    image varchar,
    roles uuid[],
    deleted boolean default false,
    created_by uuid,
    business_entity_id uuid,
    CONSTRAINT FK_entity FOREIGN KEY(business_entity_id) REFERENCES business_entities(id),
    CONSTRAINT FK_country FOREIGN KEY(country_id) REFERENCES countries(id),
    CONSTRAINT FK_admin FOREIGN KEY(created_by) REFERENCES admins(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ===========================================================================================================

CREATE TABLE IF NOT EXISTS otps(
	id uuid DEFAULT uuid_generate_v4(),
	code VARCHAR(6) NOT NULL,
	phone VARCHAR(16) NOT NULL ,
	user_type VARCHAR(10) NOT NULL ,
	expires_at TIMESTAMP NOT NULL ,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	user_id uuid,
	PRIMARY KEY (id)
);


-- ===========================================================================================================


CREATE TABLE IF NOT EXISTS insurance_companies(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	name varchar(150) not null,
	logo varchar,
    phone_numbers text[],
    emails text[],
    digital_address varchar,
    address_line_1 varchar,
    address_line_2 varchar,
    country varchar,
    created_by uuid,
    deleted boolean default false,
    CONSTRAINT FK_admin FOREIGN KEY(created_by) REFERENCES admins(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS insurance_products(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	name varchar(150) not null,
	image varchar not null,
    created_by uuid,
    deleted boolean default false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
	);

CREATE TABLE IF NOT EXISTS commissions (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    rate float not null default 0,
    agent_id uuid,
    agency_id uuid,
    cover_type varchar,
    deleted boolean default false,
    insurance_product_id uuid not null,
	created_by uuid,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_product FOREIGN KEY(insurance_product_id) REFERENCES insurance_products(id),
    CONSTRAINT FK_agent FOREIGN KEY(agent_id) REFERENCES agents(id),
    CONSTRAINT FK_agency FOREIGN KEY(agency_id) REFERENCES agencies(id),
    CONSTRAINT FK_admin FOREIGN KEY(created_by) REFERENCES admins(id),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS insurance_commissions (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    agency_rate float not null default 0,
    agent_rate float not null default 0,
    cover_type varchar,
    insurance_product_id uuid not null,
    deleted boolean default false,
    insurance_company_id uuid,
    CONSTRAINT FK_company FOREIGN KEY(insurance_company_id) REFERENCES insurance_companies(id),
    CONSTRAINT FK_product FOREIGN KEY(insurance_product_id) REFERENCES insurance_products(id),
	created_by uuid,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_admin FOREIGN KEY(created_by) REFERENCES admins(id),
    PRIMARY KEY(id)
);



CREATE TABLE IF NOT EXISTS system_commissions (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    rate float not null default 0,
    deleted boolean default false,
	created_by uuid,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_admin FOREIGN KEY(created_by) REFERENCES admins(id),
    PRIMARY KEY(id)
);



-- ===========================================================================================================


CREATE TABLE IF NOT EXISTS insurer_banks(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	insurance_company_id uuid not null,
    bank_id uuid NOT NULL,
    branch varchar, 
    account_number varchar,
    created_by uuid,
    deleted boolean default false,
    CONSTRAINT FK_agent FOREIGN KEY(created_by) REFERENCES agents(id),
    CONSTRAINT FK_bank FOREIGN KEY(bank_id) REFERENCES banks(id),
    CONSTRAINT FK_insurance_company FOREIGN KEY(insurance_company_id) REFERENCES insurance_companies(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ===========================================================================================================


CREATE TABLE IF NOT EXISTS insurance_products(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	name varchar(150) not null,
	image varchar not null,
    created_by uuid,
    deleted boolean default false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS insurance_requests (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    insurance_product_id uuid,
    registered_no varchar,
    request_data jsonb,
    requested_by uuid,
    reason varchar,
    intermediary_id uuid,
    assigned_agent_id uuid,
    assigned_agency_id uuid,
    deleted boolean default false,
    status varchar NOT NULL default 'pending',
    CONSTRAINT FK_product FOREIGN KEY(insurance_product_id) REFERENCES insurance_products(id),
    CONSTRAINT FK_customer FOREIGN KEY(requested_by) REFERENCES customers(id),
	responded_by uuid,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_agent FOREIGN KEY(responded_by) REFERENCES agents(id),
    CONSTRAINT FK_intermediary_id FOREIGN KEY(intermediary_id) REFERENCES agents(id),
    CONSTRAINT FK_assignedAgent FOREIGN KEY(assigned_agent_id) REFERENCES agents(id),
    CONSTRAINT FK_assignedAgency FOREIGN KEY(assigned_agency_id) REFERENCES agencies(id),
    PRIMARY KEY(id)
);


-- ===========================================================================================================


CREATE TABLE IF NOT EXISTS quotes (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    insurance_company_id uuid,
    insurance_request_id uuid,
    info varchar,
    premium float,
    agent_commission float,
    created_by uuid,
    deleted boolean default false,
    status varchar NOT NULL default 'pending',
    CONSTRAINT FK_company FOREIGN KEY(insurance_company_id) REFERENCES insurance_companies(id),
    CONSTRAINT FK_request FOREIGN KEY(insurance_request_id) REFERENCES insurance_requests(id),
	responded_by uuid,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT FK_agent FOREIGN KEY(created_by) REFERENCES agents(id),
    CONSTRAINT FK_customer FOREIGN KEY(responded_by) REFERENCES customers(id),
    PRIMARY KEY(id)
);

-- ===========================================================================================================

CREATE TABLE IF NOT EXISTS policies (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    quote_id uuid,
    insurance_company_id uuid,
    insurance_request_id uuid,
    start_date date not null,
    end_date date not null,
    created_by uuid,
    deleted boolean default false,
    status varchar NOT NULL default 'active',
    CONSTRAINT FK_quote FOREIGN KEY(quote_id) REFERENCES quotes(id),
    CONSTRAINT FK_company FOREIGN KEY(insurance_company_id) REFERENCES insurance_companies(id),
    CONSTRAINT FK_request FOREIGN KEY(insurance_request_id) REFERENCES insurance_requests(id),
	created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_customer FOREIGN KEY(created_by) REFERENCES customers(id),
    PRIMARY KEY(id)
);


-- ===========================================================================================================


CREATE TABLE IF NOT EXISTS form_requests (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    insurance_product_id uuid,
    request_data jsonb,
    requested_by uuid,
    reason varchar,
    vehicle_image varchar,
    vehicle_image2 varchar,
    road_doc1 varchar,
    road_doc2 varchar,
    deleted boolean default false,
    status varchar NOT NULL default 'pending',
    CONSTRAINT FK_product FOREIGN KEY(insurance_product_id) REFERENCES insurance_products(id),
    CONSTRAINT FK_customer FOREIGN KEY(requested_by) REFERENCES customers(id),
	responded_by uuid,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_admin FOREIGN KEY(responded_by) REFERENCES admins(id),
    PRIMARY KEY(id)
);

-- ===========================================================================================================


CREATE TABLE IF NOT EXISTS policy_documents(
	id uuid not null PRIMARY KEY default uuid_generate_v4(),
	document_key varchar not null,
	description varchar,
    deleted boolean default false,
    policy_id uuid,
    created_by uuid,
    created_for uuid,
    CONSTRAINT FK_policy FOREIGN KEY(policy_id) REFERENCES policies(id),
    CONSTRAINT FK_agent FOREIGN KEY(created_by) REFERENCES agents(id),
    CONSTRAINT FK_customer FOREIGN KEY(created_for) REFERENCES customers(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);






-- ===========================================================================================================


-- ===========================================================================================================
-- PAYMENT MANAGEMENT SYSTEM
-- ===========================================================================================================

CREATE TABLE IF NOT EXISTS payments(
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    quote_id uuid NOT NULL,
    policy_id uuid,
    customer_id uuid NOT NULL,
    insurance_company_id uuid NOT NULL,
    amount numeric(12,2) NOT NULL,
    payment_method varchar NOT NULL,
    client_reference varchar NOT NULL UNIQUE,
    hubtel_checkout_url varchar,
    hubtel_response jsonb,
    hubtel_callback_data jsonb,
    status varchar NOT NULL DEFAULT 'pending',
    receipt_url varchar,
    paid_at TIMESTAMP,
    deleted boolean DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_payment_quote FOREIGN KEY(quote_id) REFERENCES quotes(id),
    CONSTRAINT FK_payment_customer FOREIGN KEY(customer_id) REFERENCES customers(id),
    CONSTRAINT FK_payment_company FOREIGN KEY(insurance_company_id) REFERENCES insurance_companies(id)
);

CREATE TABLE IF NOT EXISTS transfers(
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    payment_id uuid NOT NULL,
    amount numeric(12,2) NOT NULL,
    bank_code varchar NOT NULL,
    bank_name varchar NOT NULL,
    bank_account_number varchar NOT NULL,
    bank_account_name varchar NOT NULL,
    bank_branch varchar,
    target_name varchar NOT NULL,
    client_reference varchar NOT NULL UNIQUE,
    status varchar NOT NULL DEFAULT 'pending',
    hubtel_response jsonb,
    hubtel_callback_data jsonb,
    retry_count int DEFAULT 0,
    max_retries int DEFAULT 3,
    next_retry_at TIMESTAMP,
    error_message varchar,
    completed_at TIMESTAMP,
    deleted boolean DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_transfer_payment FOREIGN KEY(payment_id) REFERENCES payments(id)
);

CREATE TABLE IF NOT EXISTS disbursement_configs(
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    insurance_company_id uuid,
    payment_method varchar NOT NULL,
    target_name varchar NOT NULL,
    bank_id uuid NOT NULL,
    bank_account_number varchar NOT NULL,
    bank_account_name varchar NOT NULL,
    bank_branch varchar,
    deleted boolean DEFAULT false,
    created_by uuid,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_disbursement_bank FOREIGN KEY(bank_id) REFERENCES banks(id),
    CONSTRAINT FK_disbursement_company FOREIGN KEY(insurance_company_id) REFERENCES insurance_companies(id)
);

CREATE TABLE IF NOT EXISTS payment_methods(
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    insurance_company_id uuid NOT NULL,
    method varchar NOT NULL,
    enabled boolean DEFAULT true,
    deleted boolean DEFAULT false,
    created_by uuid,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_pm_company FOREIGN KEY(insurance_company_id) REFERENCES insurance_companies(id)
);

CREATE TABLE IF NOT EXISTS transfer_jobs(
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    payment_id uuid NOT NULL,
    job_type varchar NOT NULL DEFAULT 'wallet_to_bank',
    status varchar NOT NULL DEFAULT 'queued',
    attempts int DEFAULT 0,
    max_attempts int DEFAULT 5,
    scheduled_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message varchar,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_job_payment FOREIGN KEY(payment_id) REFERENCES payments(id)
);

-- Payment indexes
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_customer_id ON payments(customer_id);
CREATE INDEX idx_payments_insurance_company_id ON payments(insurance_company_id);
CREATE INDEX idx_payments_created_at ON payments(created_at);
CREATE INDEX idx_transfers_payment_id ON transfers(payment_id);
CREATE INDEX idx_transfers_status ON transfers(status);
CREATE INDEX idx_transfer_jobs_status_scheduled ON transfer_jobs(status, scheduled_at);
CREATE INDEX idx_disbursement_configs_lookup ON disbursement_configs(insurance_company_id, payment_method);

-- Prevent duplicate active payments per quote
CREATE UNIQUE INDEX idx_payments_one_active_per_quote
ON payments(quote_id) WHERE status IN ('pending', 'completed');

-- Prevent duplicate disbursement configs per company+method
CREATE UNIQUE INDEX idx_disbursement_configs_unique
ON disbursement_configs(insurance_company_id, payment_method) WHERE deleted = false;

-- Prevent duplicate active transfer jobs per payment
CREATE UNIQUE INDEX idx_transfer_jobs_one_per_payment
ON transfer_jobs(payment_id) WHERE status IN ('queued', 'processing', 'completed');