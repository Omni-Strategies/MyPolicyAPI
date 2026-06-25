from typing import Optional
import datetime
import decimal
import enum
import uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ARRAY, Boolean, Date, DateTime, Double, Enum, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class GenderEnum(str, enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class Admins(Base):
    __tablename__ = 'admins'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='admins_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    email: Mapped[Optional[str]] = mapped_column(String)
    image: Mapped[Optional[str]] = mapped_column(String)
    department: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[Optional[str]] = mapped_column(String, server_default=text("'active'::character varying"))
    password: Mapped[Optional[str]] = mapped_column(String)
    roles: Mapped[Optional[list[uuid.UUID]]] = mapped_column(ARRAY(Uuid()))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    agents: Mapped[list['Agents']] = relationship('Agents', back_populates='admins')
    banks: Mapped[list['Banks']] = relationship('Banks', back_populates='admins')
    business_entities: Mapped[list['BusinessEntities']] = relationship('BusinessEntities', back_populates='admins')
    insurance_companies: Mapped[list['InsuranceCompanies']] = relationship('InsuranceCompanies', back_populates='admins')
    system_commissions: Mapped[list['SystemCommissions']] = relationship('SystemCommissions', back_populates='admins')
    vehicle_makes: Mapped[list['VehicleMakes']] = relationship('VehicleMakes', back_populates='admins')
    commissions: Mapped[list['Commissions']] = relationship('Commissions', back_populates='admins')
    customers: Mapped[list['Customers']] = relationship('Customers', back_populates='admins')
    insurance_commissions: Mapped[list['InsuranceCommissions']] = relationship('InsuranceCommissions', back_populates='admins')
    vehicle_models: Mapped[list['VehicleModels']] = relationship('VehicleModels', back_populates='admins')
    form_requests: Mapped[list['FormRequests']] = relationship('FormRequests', back_populates='admins')


class Agencies(Base):
    __tablename__ = 'agencies'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='agencies_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    logo: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    agents: Mapped[list['Agents']] = relationship('Agents', back_populates='organization')
    roles: Mapped[list['Roles']] = relationship('Roles', back_populates='organization')
    commissions: Mapped[list['Commissions']] = relationship('Commissions', back_populates='agency')
    permissions: Mapped[list['Permissions']] = relationship('Permissions', back_populates='organization')
    insurance_requests: Mapped[list['InsuranceRequests']] = relationship('InsuranceRequests', back_populates='assigned_agency')


class AgentRequests(Base):
    __tablename__ = 'agent_requests'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='agent_requests_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    request_type: Mapped[str] = mapped_column(String, nullable=False)
    request_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    status: Mapped[Optional[str]] = mapped_column(String, server_default=text("'pending'::character varying"))
    reason: Mapped[Optional[str]] = mapped_column(String)
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)


class Countries(Base):
    __tablename__ = 'countries'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='countries_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    code: Mapped[Optional[str]] = mapped_column(String)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    agents: Mapped[list['Agents']] = relationship('Agents', back_populates='country')
    customers: Mapped[list['Customers']] = relationship('Customers', back_populates='country')


class InsuranceProducts(Base):
    __tablename__ = 'insurance_products'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='insurance_products_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    commissions: Mapped[list['Commissions']] = relationship('Commissions', back_populates='insurance_product')
    insurance_commissions: Mapped[list['InsuranceCommissions']] = relationship('InsuranceCommissions', back_populates='insurance_product')
    form_requests: Mapped[list['FormRequests']] = relationship('FormRequests', back_populates='insurance_product')
    insurance_requests: Mapped[list['InsuranceRequests']] = relationship('InsuranceRequests', back_populates='insurance_product')


class Otps(Base):
    __tablename__ = 'otps'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='otps_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    phone: Mapped[str] = mapped_column(String(16), nullable=False)
    user_type: Mapped[str] = mapped_column(String(10), nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)


class Agents(Base):
    __tablename__ = 'agents'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['countries.id'], name='fk_country'),
        ForeignKeyConstraint(['created_by'], ['admins.id'], name='fk_admin'),
        ForeignKeyConstraint(['organization_id'], ['agencies.id'], name='fk_organization'),
        PrimaryKeyConstraint('id', name='agents_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str] = mapped_column(String(16), nullable=False)
    digital_address: Mapped[str] = mapped_column(String, nullable=False)
    physical_address: Mapped[str] = mapped_column(String, nullable=False)
    postal_address: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, server_default=text("'active'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    email: Mapped[Optional[str]] = mapped_column(String)
    intermediary_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    intermediary_type: Mapped[Optional[str]] = mapped_column(String, server_default=text("'agent'::character varying"))
    agent_code: Mapped[Optional[str]] = mapped_column(String)
    image: Mapped[Optional[str]] = mapped_column(String)
    nic_document: Mapped[Optional[str]] = mapped_column(String)
    agreement_document: Mapped[Optional[str]] = mapped_column(String)
    country_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    password: Mapped[Optional[str]] = mapped_column(String)
    roles: Mapped[Optional[list[uuid.UUID]]] = mapped_column(ARRAY(Uuid()))
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    country: Mapped[Optional['Countries']] = relationship('Countries', back_populates='agents')
    admins: Mapped[Optional['Admins']] = relationship('Admins', back_populates='agents')
    organization: Mapped[Optional['Agencies']] = relationship('Agencies', back_populates='agents')
    commissions: Mapped[list['Commissions']] = relationship('Commissions', back_populates='agent')
    insurer_banks: Mapped[list['InsurerBanks']] = relationship('InsurerBanks', back_populates='agents')
    insurance_requests_assigned_agent: Mapped[list['InsuranceRequests']] = relationship('InsuranceRequests', foreign_keys='[InsuranceRequests.assigned_agent_id]', back_populates='assigned_agent')
    insurance_requests_intermediary: Mapped[list['InsuranceRequests']] = relationship('InsuranceRequests', foreign_keys='[InsuranceRequests.intermediary_id]', back_populates='intermediary')
    insurance_requests_responded_by: Mapped[list['InsuranceRequests']] = relationship('InsuranceRequests', foreign_keys='[InsuranceRequests.responded_by]', back_populates='agents')
    quotes: Mapped[list['Quotes']] = relationship('Quotes', back_populates='agents')
    policy_documents: Mapped[list['PolicyDocuments']] = relationship('PolicyDocuments', back_populates='agents')


class Banks(Base):
    __tablename__ = 'banks'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['admins.id'], name='fk_admin'),
        PrimaryKeyConstraint('id', name='banks_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    bank_code: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    admins: Mapped[Optional['Admins']] = relationship('Admins', back_populates='banks')
    disbursement_configs: Mapped[list['DisbursementConfigs']] = relationship('DisbursementConfigs', back_populates='bank')
    insurer_banks: Mapped[list['InsurerBanks']] = relationship('InsurerBanks', back_populates='bank')


class BusinessEntities(Base):
    __tablename__ = 'business_entities'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['admins.id'], name='fk_admin'),
        PrimaryKeyConstraint('id', name='business_entities_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    logo: Mapped[str] = mapped_column(String, nullable=False)
    tin_no: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    admins: Mapped[Optional['Admins']] = relationship('Admins', back_populates='business_entities')
    customers: Mapped[list['Customers']] = relationship('Customers', back_populates='business_entity')


class InsuranceCompanies(Base):
    __tablename__ = 'insurance_companies'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['admins.id'], name='fk_admin'),
        PrimaryKeyConstraint('id', name='insurance_companies_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    logo: Mapped[Optional[str]] = mapped_column(String)
    phone_numbers: Mapped[Optional[list[str]]] = mapped_column(ARRAY(Text()))
    emails: Mapped[Optional[list[str]]] = mapped_column(ARRAY(Text()))
    digital_address: Mapped[Optional[str]] = mapped_column(String)
    address_line_1: Mapped[Optional[str]] = mapped_column(String)
    address_line_2: Mapped[Optional[str]] = mapped_column(String)
    country: Mapped[Optional[str]] = mapped_column(String)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    admins: Mapped[Optional['Admins']] = relationship('Admins', back_populates='insurance_companies')
    disbursement_configs: Mapped[list['DisbursementConfigs']] = relationship('DisbursementConfigs', back_populates='insurance_company')
    insurance_commissions: Mapped[list['InsuranceCommissions']] = relationship('InsuranceCommissions', back_populates='insurance_company')
    insurer_banks: Mapped[list['InsurerBanks']] = relationship('InsurerBanks', back_populates='insurance_company')
    payment_methods: Mapped[list['PaymentMethods']] = relationship('PaymentMethods', back_populates='insurance_company')
    quotes: Mapped[list['Quotes']] = relationship('Quotes', back_populates='insurance_company')
    payments: Mapped[list['Payments']] = relationship('Payments', back_populates='insurance_company')
    policies: Mapped[list['Policies']] = relationship('Policies', back_populates='insurance_company')


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['agencies.id'], name='fk_organization'),
        PrimaryKeyConstraint('id', name='roles_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    role_type: Mapped[Optional[str]] = mapped_column(String)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    organization: Mapped[Optional['Agencies']] = relationship('Agencies', back_populates='roles')
    permissions: Mapped[list['Permissions']] = relationship('Permissions', back_populates='role')


class SystemCommissions(Base):
    __tablename__ = 'system_commissions'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['admins.id'], name='fk_admin'),
        PrimaryKeyConstraint('id', name='system_commissions_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    rate: Mapped[float] = mapped_column(Double(53), nullable=False, server_default=text('0'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    admins: Mapped[Optional['Admins']] = relationship('Admins', back_populates='system_commissions')


class VehicleMakes(Base):
    __tablename__ = 'vehicle_makes'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['admins.id'], name='fk_admin'),
        PrimaryKeyConstraint('id', name='vehicle_makes_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    models: Mapped[Optional[list[dict]]] = mapped_column(ARRAY(JSONB()))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    admins: Mapped[Optional['Admins']] = relationship('Admins', back_populates='vehicle_makes')
    vehicle_models: Mapped[list['VehicleModels']] = relationship('VehicleModels', back_populates='make')


class Commissions(Base):
    __tablename__ = 'commissions'
    __table_args__ = (
        ForeignKeyConstraint(['agency_id'], ['agencies.id'], name='fk_agency'),
        ForeignKeyConstraint(['agent_id'], ['agents.id'], name='fk_agent'),
        ForeignKeyConstraint(['created_by'], ['admins.id'], name='fk_admin'),
        ForeignKeyConstraint(['insurance_product_id'], ['insurance_products.id'], name='fk_product'),
        PrimaryKeyConstraint('id', name='commissions_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    rate: Mapped[float] = mapped_column(Double(53), nullable=False, server_default=text('0'))
    insurance_product_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    agency_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    cover_type: Mapped[Optional[str]] = mapped_column(String)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    agency: Mapped[Optional['Agencies']] = relationship('Agencies', back_populates='commissions')
    agent: Mapped[Optional['Agents']] = relationship('Agents', back_populates='commissions')
    admins: Mapped[Optional['Admins']] = relationship('Admins', back_populates='commissions')
    insurance_product: Mapped['InsuranceProducts'] = relationship('InsuranceProducts', back_populates='commissions')


class Customers(Base):
    __tablename__ = 'customers'
    __table_args__ = (
        ForeignKeyConstraint(['business_entity_id'], ['business_entities.id'], name='fk_entity'),
        ForeignKeyConstraint(['country_id'], ['countries.id'], name='fk_country'),
        ForeignKeyConstraint(['created_by'], ['admins.id'], name='fk_admin'),
        PrimaryKeyConstraint('id', name='customers_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    email: Mapped[Optional[str]] = mapped_column(String)
    digital_address: Mapped[Optional[str]] = mapped_column(String)
    gender: Mapped[Optional[GenderEnum]] = mapped_column(Enum(GenderEnum, values_callable=lambda cls: [member.value for member in cls], name='gender_enum'), server_default=text("'male'::gender_enum"))
    customer_type: Mapped[Optional[str]] = mapped_column(String)
    gh_card_no: Mapped[Optional[str]] = mapped_column(String)
    country_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    dob: Mapped[Optional[str]] = mapped_column(String)
    password: Mapped[Optional[str]] = mapped_column(String)

    image: Mapped[Optional[dict]] = mapped_column(JSONB)        
    roles: Mapped[Optional[list[uuid.UUID]]] = mapped_column(ARRAY(Uuid()))
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    business_entity_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    business_entity: Mapped[Optional['BusinessEntities']] = relationship('BusinessEntities', back_populates='customers')
    country: Mapped[Optional['Countries']] = relationship('Countries', back_populates='customers')
    admins: Mapped[Optional['Admins']] = relationship('Admins', back_populates='customers')
    form_requests: Mapped[list['FormRequests']] = relationship('FormRequests', back_populates='customers')
    insurance_requests: Mapped[list['InsuranceRequests']] = relationship('InsuranceRequests', back_populates='customers')
    quotes: Mapped[list['Quotes']] = relationship('Quotes', back_populates='customers')
    payments: Mapped[list['Payments']] = relationship('Payments', back_populates='customer')
    policies: Mapped[list['Policies']] = relationship('Policies', back_populates='customers')
    policy_documents: Mapped[list['PolicyDocuments']] = relationship('PolicyDocuments', back_populates='customers')


class DisbursementConfigs(Base):
    __tablename__ = 'disbursement_configs'
    __table_args__ = (
        ForeignKeyConstraint(['bank_id'], ['banks.id'], name='fk_disbursement_bank'),
        ForeignKeyConstraint(['insurance_company_id'], ['insurance_companies.id'], name='fk_disbursement_company'),
        PrimaryKeyConstraint('id', name='disbursement_configs_pkey'),
        Index('idx_disbursement_configs_lookup', 'insurance_company_id', 'payment_method'),
        Index('idx_disbursement_configs_unique', 'insurance_company_id', 'payment_method', postgresql_where='(deleted = false)', unique=True)
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    payment_method: Mapped[str] = mapped_column(String, nullable=False)
    target_name: Mapped[str] = mapped_column(String, nullable=False)
    bank_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    bank_account_number: Mapped[str] = mapped_column(String, nullable=False)
    bank_account_name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    insurance_company_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    bank_branch: Mapped[Optional[str]] = mapped_column(String)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    bank: Mapped['Banks'] = relationship('Banks', back_populates='disbursement_configs')
    insurance_company: Mapped[Optional['InsuranceCompanies']] = relationship('InsuranceCompanies', back_populates='disbursement_configs')


class InsuranceCommissions(Base):
    __tablename__ = 'insurance_commissions'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['admins.id'], name='fk_admin'),
        ForeignKeyConstraint(['insurance_company_id'], ['insurance_companies.id'], name='fk_company'),
        ForeignKeyConstraint(['insurance_product_id'], ['insurance_products.id'], name='fk_product'),
        PrimaryKeyConstraint('id', name='insurance_commissions_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    agency_rate: Mapped[float] = mapped_column(Double(53), nullable=False, server_default=text('0'))
    agent_rate: Mapped[float] = mapped_column(Double(53), nullable=False, server_default=text('0'))
    insurance_product_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    cover_type: Mapped[Optional[str]] = mapped_column(String)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    insurance_company_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    admins: Mapped[Optional['Admins']] = relationship('Admins', back_populates='insurance_commissions')
    insurance_company: Mapped[Optional['InsuranceCompanies']] = relationship('InsuranceCompanies', back_populates='insurance_commissions')
    insurance_product: Mapped['InsuranceProducts'] = relationship('InsuranceProducts', back_populates='insurance_commissions')


class InsurerBanks(Base):
    __tablename__ = 'insurer_banks'
    __table_args__ = (
        ForeignKeyConstraint(['bank_id'], ['banks.id'], name='fk_bank'),
        ForeignKeyConstraint(['created_by'], ['agents.id'], name='fk_agent'),
        ForeignKeyConstraint(['insurance_company_id'], ['insurance_companies.id'], name='fk_insurance_company'),
        PrimaryKeyConstraint('id', name='insurer_banks_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    insurance_company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    bank_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    branch: Mapped[Optional[str]] = mapped_column(String)
    account_number: Mapped[Optional[str]] = mapped_column(String)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    bank: Mapped['Banks'] = relationship('Banks', back_populates='insurer_banks')
    agents: Mapped[Optional['Agents']] = relationship('Agents', back_populates='insurer_banks')
    insurance_company: Mapped['InsuranceCompanies'] = relationship('InsuranceCompanies', back_populates='insurer_banks')


class PaymentMethods(Base):
    __tablename__ = 'payment_methods'
    __table_args__ = (
        ForeignKeyConstraint(['insurance_company_id'], ['insurance_companies.id'], name='fk_pm_company'),
        PrimaryKeyConstraint('id', name='payment_methods_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    insurance_company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    method: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    enabled: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    insurance_company: Mapped['InsuranceCompanies'] = relationship('InsuranceCompanies', back_populates='payment_methods')


class Permissions(Base):
    __tablename__ = 'permissions'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['agencies.id'], name='fk_organization'),
        ForeignKeyConstraint(['role_id'], ['roles.id'], name='fk_role'),
        PrimaryKeyConstraint('id', name='permissions_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    module: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    role_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    organization: Mapped[Optional['Agencies']] = relationship('Agencies', back_populates='permissions')
    role: Mapped[Optional['Roles']] = relationship('Roles', back_populates='permissions')


class VehicleModels(Base):
    __tablename__ = 'vehicle_models'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['admins.id'], name='fk_admin'),
        ForeignKeyConstraint(['make_id'], ['vehicle_makes.id'], name='fk_make'),
        PrimaryKeyConstraint('id', name='vehicle_models_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    make_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    admins: Mapped[Optional['Admins']] = relationship('Admins', back_populates='vehicle_models')
    make: Mapped[Optional['VehicleMakes']] = relationship('VehicleMakes', back_populates='vehicle_models')


class FormRequests(Base):
    __tablename__ = 'form_requests'
    __table_args__ = (
        ForeignKeyConstraint(['insurance_product_id'], ['insurance_products.id'], name='fk_product'),
        ForeignKeyConstraint(['requested_by'], ['customers.id'], name='fk_customer'),
        ForeignKeyConstraint(['responded_by'], ['admins.id'], name='fk_admin'),
        PrimaryKeyConstraint('id', name='form_requests_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    status: Mapped[str] = mapped_column(String, nullable=False, server_default=text("'pending'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    insurance_product_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    request_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    requested_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    reason: Mapped[Optional[str]] = mapped_column(String)
    vehicle_image: Mapped[Optional[dict]] = mapped_column(JSONB)
    vehicle_image2: Mapped[Optional[dict]] = mapped_column(JSONB)
    road_doc1: Mapped[Optional[dict]] = mapped_column(JSONB)
    road_doc2: Mapped[Optional[dict]] = mapped_column(JSONB)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    responded_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    insurance_product: Mapped[Optional['InsuranceProducts']] = relationship('InsuranceProducts', back_populates='form_requests')
    customers: Mapped[Optional['Customers']] = relationship('Customers', back_populates='form_requests')
    admins: Mapped[Optional['Admins']] = relationship('Admins', back_populates='form_requests')


class InsuranceRequests(Base):
    __tablename__ = 'insurance_requests'
    __table_args__ = (
        ForeignKeyConstraint(['assigned_agency_id'], ['agencies.id'], name='fk_assignedagency'),
        ForeignKeyConstraint(['assigned_agent_id'], ['agents.id'], name='fk_assignedagent'),
        ForeignKeyConstraint(['insurance_product_id'], ['insurance_products.id'], name='fk_product'),
        ForeignKeyConstraint(['intermediary_id'], ['agents.id'], name='fk_intermediary_id'),
        ForeignKeyConstraint(['requested_by'], ['customers.id'], name='fk_customer'),
        ForeignKeyConstraint(['responded_by'], ['agents.id'], name='fk_agent'),
        PrimaryKeyConstraint('id', name='insurance_requests_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    status: Mapped[str] = mapped_column(String, nullable=False, server_default=text("'pending'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    insurance_product_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    registered_no: Mapped[Optional[str]] = mapped_column(String)
    request_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    requested_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    reason: Mapped[Optional[str]] = mapped_column(String)
    intermediary_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    assigned_agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    assigned_agency_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    responded_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    assigned_agency: Mapped[Optional['Agencies']] = relationship('Agencies', back_populates='insurance_requests')
    assigned_agent: Mapped[Optional['Agents']] = relationship('Agents', foreign_keys=[assigned_agent_id], back_populates='insurance_requests_assigned_agent')
    insurance_product: Mapped[Optional['InsuranceProducts']] = relationship('InsuranceProducts', back_populates='insurance_requests')
    intermediary: Mapped[Optional['Agents']] = relationship('Agents', foreign_keys=[intermediary_id], back_populates='insurance_requests_intermediary')
    customers: Mapped[Optional['Customers']] = relationship('Customers', back_populates='insurance_requests')
    agents: Mapped[Optional['Agents']] = relationship('Agents', foreign_keys=[responded_by], back_populates='insurance_requests_responded_by')
    quotes: Mapped[list['Quotes']] = relationship('Quotes', back_populates='insurance_request')
    policies: Mapped[list['Policies']] = relationship('Policies', back_populates='insurance_request')


class Quotes(Base):
    __tablename__ = 'quotes'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['agents.id'], name='fk_agent'),
        ForeignKeyConstraint(['insurance_company_id'], ['insurance_companies.id'], name='fk_company'),
        ForeignKeyConstraint(['insurance_request_id'], ['insurance_requests.id'], name='fk_request'),
        ForeignKeyConstraint(['responded_by'], ['customers.id'], name='fk_customer'),
        PrimaryKeyConstraint('id', name='quotes_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    status: Mapped[str] = mapped_column(String, nullable=False, server_default=text("'pending'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    insurance_company_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    insurance_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    info: Mapped[Optional[str]] = mapped_column(String)
    premium: Mapped[Optional[float]] = mapped_column(Double(53))
    agent_commission: Mapped[Optional[float]] = mapped_column(Double(53))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    responded_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    agents: Mapped[Optional['Agents']] = relationship('Agents', back_populates='quotes')
    insurance_company: Mapped[Optional['InsuranceCompanies']] = relationship('InsuranceCompanies', back_populates='quotes')
    insurance_request: Mapped[Optional['InsuranceRequests']] = relationship('InsuranceRequests', back_populates='quotes')
    customers: Mapped[Optional['Customers']] = relationship('Customers', back_populates='quotes')
    payments: Mapped[list['Payments']] = relationship('Payments', back_populates='quote')
    policies: Mapped[list['Policies']] = relationship('Policies', back_populates='quote')


class Payments(Base):
    __tablename__ = 'payments'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customers.id'], name='fk_payment_customer'),
        ForeignKeyConstraint(['insurance_company_id'], ['insurance_companies.id'], name='fk_payment_company'),
        ForeignKeyConstraint(['quote_id'], ['quotes.id'], name='fk_payment_quote'),
        PrimaryKeyConstraint('id', name='payments_pkey'),
        UniqueConstraint('client_reference', name='payments_client_reference_key'),
        Index('idx_payments_created_at', 'created_at'),
        Index('idx_payments_customer_id', 'customer_id'),
        Index('idx_payments_insurance_company_id', 'insurance_company_id'),
        Index('idx_payments_one_active_per_quote', 'quote_id', postgresql_where="((status)::text = ANY ((ARRAY['pending'::character varying, 'completed'::character varying])::text[]))", unique=True),
        Index('idx_payments_status', 'status')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    quote_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    customer_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    insurance_company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String, nullable=False)
    client_reference: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, server_default=text("'pending'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    policy_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    hubtel_checkout_url: Mapped[Optional[str]] = mapped_column(String)
    hubtel_response: Mapped[Optional[dict]] = mapped_column(JSONB)
    hubtel_callback_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    receipt_url: Mapped[Optional[str]] = mapped_column(String)
    paid_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    customer: Mapped['Customers'] = relationship('Customers', back_populates='payments')
    insurance_company: Mapped['InsuranceCompanies'] = relationship('InsuranceCompanies', back_populates='payments')
    quote: Mapped['Quotes'] = relationship('Quotes', back_populates='payments')
    transfer_jobs: Mapped[list['TransferJobs']] = relationship('TransferJobs', back_populates='payment')
    transfers: Mapped[list['Transfers']] = relationship('Transfers', back_populates='payment')


class Policies(Base):
    __tablename__ = 'policies'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['customers.id'], name='fk_customer'),
        ForeignKeyConstraint(['insurance_company_id'], ['insurance_companies.id'], name='fk_company'),
        ForeignKeyConstraint(['insurance_request_id'], ['insurance_requests.id'], name='fk_request'),
        ForeignKeyConstraint(['quote_id'], ['quotes.id'], name='fk_quote'),
        PrimaryKeyConstraint('id', name='policies_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, server_default=text("'active'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    quote_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    insurance_company_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    insurance_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    customers: Mapped[Optional['Customers']] = relationship('Customers', back_populates='policies')
    insurance_company: Mapped[Optional['InsuranceCompanies']] = relationship('InsuranceCompanies', back_populates='policies')
    insurance_request: Mapped[Optional['InsuranceRequests']] = relationship('InsuranceRequests', back_populates='policies')
    quote: Mapped[Optional['Quotes']] = relationship('Quotes', back_populates='policies')
    policy_documents: Mapped[list['PolicyDocuments']] = relationship('PolicyDocuments', back_populates='policy')


class PolicyDocuments(Base):
    __tablename__ = 'policy_documents'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['agents.id'], name='fk_agent'),
        ForeignKeyConstraint(['created_for'], ['customers.id'], name='fk_customer'),
        ForeignKeyConstraint(['policy_id'], ['policies.id'], name='fk_policy'),
        PrimaryKeyConstraint('id', name='policy_documents_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    document_key: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    description: Mapped[Optional[str]] = mapped_column(String)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    policy_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_for: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    agents: Mapped[Optional['Agents']] = relationship('Agents', back_populates='policy_documents')
    customers: Mapped[Optional['Customers']] = relationship('Customers', back_populates='policy_documents')
    policy: Mapped[Optional['Policies']] = relationship('Policies', back_populates='policy_documents')


class TransferJobs(Base):
    __tablename__ = 'transfer_jobs'
    __table_args__ = (
        ForeignKeyConstraint(['payment_id'], ['payments.id'], name='fk_job_payment'),
        PrimaryKeyConstraint('id', name='transfer_jobs_pkey'),
        Index('idx_transfer_jobs_one_per_payment', 'payment_id', postgresql_where="((status)::text = ANY ((ARRAY['queued'::character varying, 'processing'::character varying, 'completed'::character varying])::text[]))", unique=True),
        Index('idx_transfer_jobs_status_scheduled', 'status', 'scheduled_at')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    payment_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    job_type: Mapped[str] = mapped_column(String, nullable=False, server_default=text("'wallet_to_bank'::character varying"))
    status: Mapped[str] = mapped_column(String, nullable=False, server_default=text("'queued'::character varying"))
    scheduled_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    attempts: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    max_attempts: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('5'))
    started_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    error_message: Mapped[Optional[str]] = mapped_column(String)

    payment: Mapped['Payments'] = relationship('Payments', back_populates='transfer_jobs')


class Transfers(Base):
    __tablename__ = 'transfers'
    __table_args__ = (
        ForeignKeyConstraint(['payment_id'], ['payments.id'], name='fk_transfer_payment'),
        PrimaryKeyConstraint('id', name='transfers_pkey'),
        UniqueConstraint('client_reference', name='transfers_client_reference_key'),
        Index('idx_transfers_payment_id', 'payment_id'),
        Index('idx_transfers_status', 'status')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    payment_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    bank_code: Mapped[str] = mapped_column(String, nullable=False)
    bank_name: Mapped[str] = mapped_column(String, nullable=False)
    bank_account_number: Mapped[str] = mapped_column(String, nullable=False)
    bank_account_name: Mapped[str] = mapped_column(String, nullable=False)
    target_name: Mapped[str] = mapped_column(String, nullable=False)
    client_reference: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, server_default=text("'pending'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    bank_branch: Mapped[Optional[str]] = mapped_column(String)
    hubtel_response: Mapped[Optional[dict]] = mapped_column(JSONB)
    hubtel_callback_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    retry_count: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    max_retries: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('3'))
    next_retry_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    error_message: Mapped[Optional[str]] = mapped_column(String)
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    payment: Mapped['Payments'] = relationship('Payments', back_populates='transfers')
