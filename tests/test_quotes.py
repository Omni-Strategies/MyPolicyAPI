import pytest
from unittest.mock import MagicMock
from models.models import Quotes
from repositories.quotes_repo import (create_quote, get_quote, update_quote, delete_quote)


def test_create_quote_success():
    mock_session = MagicMock()
    mock_quote = MagicMock()
    mock_quote.dict.return_value = {"insurance_request_id": "Q123", "premium": 1000.0, "agent_commission": 100.0}
    company_id = "C123"
    create_quote(mock_session, mock_quote, company_id)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_quote_fail():
    mock_session = MagicMock()
    mock_quote = MagicMock()
    mock_quote.dict.return_value = {"insurance_request_id": "Q123", "premium": 1000.0, "company_id": "C123", "agent_commission": 100.0}
    mock_session.commit.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        create_quote(mock_session, mock_quote)

def test_get_quote_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    result = get_quote(mock_session, 1)
    mock_session.query.return_value.filter.assert_called_once()
    assert result is None

def test_get_quote_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        get_quote(mock_session, 1)

def test_get_quote_success():
    mock_session = MagicMock()
    mock_quote = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_quote
    result = get_quote(mock_session, 1)
    mock_session.query.return_value.filter.assert_called_once()
    assert result == mock_quote

def test_update_quote_success():
    mock_session = MagicMock()
    mock_quote = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_quote
    mock_update_data = MagicMock()
    mock_update_data.dict.return_value = {"premium": 1200.0, "company_id": "C123", "agent_commission": 100.0}
    mock_session.commit.return_value = None
    result = update_quote(mock_session, mock_update_data, 1)
    
    mock_session.query.return_value.filter.assert_called_once()
    assert result == mock_quote
    assert mock_quote.premium == 1200.0
    assert mock_quote.company_id == "C123"
    assert mock_quote.agent_commission == 100.0
    mock_session.commit.assert_called_once()

def test_update_quote_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_update_data = MagicMock()
    with pytest.raises(Exception):
        update_quote(mock_session, mock_update_data)

def test_update_quote_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    mock_update_data = MagicMock()
    with pytest.raises(Exception):
        update_quote(mock_session, mock_update_data, 1)
        mock_session.commit.assert_not_called()

def test_delete_quote_success():
    mock_session = MagicMock()
    mock_quote = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_quote
    mock_session.commit.return_value = None
    result = delete_quote(mock_session, 1)
    
    mock_session.query.return_value.filter.assert_called_once()
    assert result is True
    mock_session.delete.assert_called_once_with(mock_quote)
    mock_session.commit.assert_called_once()

def test_delete_quote_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    result = delete_quote(mock_session, 1)
    assert result is False

def test_delete_quote_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        delete_quote(mock_session, 1)
        mock_session.commit.assert_not_called()
