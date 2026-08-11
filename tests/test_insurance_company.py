import pytest
from unittest.mock import MagicMock
from models.models import InsuranceCompanies
from repositories.insurance_company_repo import (create_insurance_company, get_insurance_company_by_email, get_insurance_company_by_id, update_insurance_company, delete_insurance_company)   

def test_create_insurance_company_success():
    mock_session = MagicMock()
    mock_company = MagicMock()
    mock_company.dict.return_value = {"name": "Test Insurance", "address_line_1": "123 Test St", "emails": "[test@example.com]", "phone_numbers": ["123-456-7890"], "digital_address": "DA-123", "country": "Testland"}
    create_insurance_company(mock_session, mock_company)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_insurance_company_fail():
    mock_session = MagicMock()
    mock_company = MagicMock()
    mock_company.dict.return_value = {"name": "Test Insurance", "address_line_1": "123 Test St", "emails": "[test@example.com]", "phone_numbers": ["123-456-7890"], "digital_address": "DA-123", "country": "Testland"}
    mock_session.add.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        create_insurance_company(mock_session, mock_company)    

def test_get_insurance_company_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    result = get_insurance_company_by_id(mock_session, 1)
    mock_session.query.return_value.filter.assert_called_once()
    assert result is None

def test_get_insurance_company_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        get_insurance_company_by_id(mock_session, 1)   

def test_get_insurance_company_success():
    mock_session = MagicMock()
    mock_company = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_company
    result = get_insurance_company_by_id(mock_session, 1)
    mock_session.query.return_value.filter.assert_called_once()
    assert result == mock_company

def test_update_insurance_company_success():
    mock_session = MagicMock()
    mock_company = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_company
    mock_update_data = MagicMock()
    mock_update_data.dict.return_value = {"address_line_1": "456 New St"}
    mock_session.commit.return_value = None
    result = update_insurance_company(mock_session, 1, mock_update_data)

    mock_session.query.return_value.filter.assert_called_once()
    assert result == mock_company
    assert mock_company.address_line_1 == "456 New St"
    mock_session.commit.assert_called_once()

def test_update_insurance_company_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_update_data = MagicMock()
    mock_update_data.dict.return_value = {"address_line_1": "456 New St"}
    result = update_insurance_company(mock_session, 1, mock_update_data)

    mock_session.query.return_value.filter.assert_called_once()
    assert result is None
    mock_session.commit.assert_not_called()

def test_update_insurance_company_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    mock_update_data = MagicMock()
    mock_update_data.dict.return_value = {"address_line_1": "456 New St"}
    with pytest.raises(Exception):
        update_insurance_company(mock_session, 1, mock_update_data)

def test_delete_insurance_company_success():
    mock_session = MagicMock()
    mock_company = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_company
    mock_session.commit.return_value = None
    result = delete_insurance_company(mock_session, 1)
    
    mock_session.query.return_value.filter.assert_called_once()
    assert result is True
    mock_session.delete.assert_called_once_with(mock_company)
    mock_session.commit.assert_called_once()

def test_delete_insurance_company_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    result = delete_insurance_company(mock_session, 1)
    
    mock_session.query.return_value.filter.assert_called_once()
    assert result is False
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()

def test_delete_insurance_company_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        delete_insurance_company(mock_session, 1)

def test_get_insurance_company_by_email_success():
    mock_session = MagicMock()
    mock_company = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_company
    result = get_insurance_company_by_email(mock_session, "test@example.com")
    mock_session.query.return_value.filter.assert_called_once()
    assert result == mock_company