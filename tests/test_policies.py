import pytest
from unittest.mock import MagicMock
from models.models import Policies
from repositories.policies_repo import (make_request_status_to_paid, make_request_into_policy)


def test_make_request_status_to_paid_success():
    mock_session = MagicMock()
    mock_request = MagicMock()
    mock_request.status = "pending"
    mock_session.query.return_value.filter.return_value.first.return_value = mock_request

    result = make_request_status_to_paid(mock_session, "request_id")
    
    assert result.status == "paid"
    mock_session.commit.assert_called_once(
    )

def test_make_request_status_to_paid_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None

    result = make_request_status_to_paid(mock_session, "request_id")
    
    assert result is None
    mock_session.commit.assert_not_called()

def test_make_request_status_to_paid_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    
    with pytest.raises(Exception):
        make_request_status_to_paid(mock_session, "request_id")

def test_make_request_into_policy_success():
    mock_session = MagicMock()
    mock_request = MagicMock()
    mock_request.request_data = {"policy": {"startDate": "2026-04-18", "duration": "12"}}
    mock_quote = MagicMock()
    mock_company = MagicMock()
    mock_customer = MagicMock()

    mock_session.query.return_value.filter.side_effect = [
        MagicMock(first=MagicMock(return_value=mock_request)),  # For InsuranceRequests
        MagicMock(first=MagicMock(return_value=mock_quote)),    # For Quotes
        MagicMock(first=MagicMock(return_value=mock_company)),  # For InsuranceCompanies
        MagicMock(first=MagicMock(return_value=mock_customer))  # For Customers
    ]
    request_id = "123"
    result = make_request_into_policy(mock_session, request_id)
    
    assert isinstance(result, Policies)
    mock_session.commit.assert_called_once()

def test_make_request_into_policy_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None

    result = make_request_into_policy(mock_session, "request_id")
    
    assert result is None
    mock_session.commit.assert_not_called()

def test_make_request_into_policy_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    
    with pytest.raises(Exception):
        make_request_into_policy(mock_session, "request_id")


def test_make_request_into_policy_no_quote():
    mock_session = MagicMock()
    mock_request = MagicMock()
    mock_session.query.return_value.filter.side_effect = [
        MagicMock(first=MagicMock(return_value=mock_request)),  # For InsuranceRequests
        MagicMock(first=MagicMock(return_value=None))           # For Quotes (no quote found)
    ]

    result = make_request_into_policy(mock_session, "request_id")
    
    assert result is None
    mock_session.commit.assert_not_called()

def test_make_request_into_policy_no_company():
    mock_session = MagicMock()
    mock_request = MagicMock()
    mock_quote = MagicMock()
    mock_session.query.return_value.filter.side_effect = [
        MagicMock(first=MagicMock(return_value=mock_request)),  # For InsuranceRequests
        MagicMock(first=MagicMock(return_value=mock_quote)),    # For Quotes
        MagicMock(first=MagicMock(return_value=None))           # For InsuranceCompanies (no company found)
    ]

    result = make_request_into_policy(mock_session, "request_id")
    
    assert result is None
    mock_session.commit.assert_not_called()

