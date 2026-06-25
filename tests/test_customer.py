import pytest
from unittest.mock import MagicMock
from models.models import Customers
from repositories.customer_repo import (create_customer, get_customer, update_customer, delete_customer)

def test_create_customer_success():
    mock_session = MagicMock()
    mock_customer = MagicMock()
    mock_customer.dict.return_value = {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"} 
    create_customer(mock_session, mock_customer)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_customer_fail():
    mock_session = MagicMock()
    mock_customer = MagicMock()
    mock_customer.dict.return_value = {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}
    mock_session.commit.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        create_customer(mock_session, mock_customer)


def test_get_customer_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    result = get_customer(mock_session, 1)
    mock_session.query.return_value.filter.assert_called_once()
    assert result is None

def test_get_customer_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        get_customer(mock_session, 1)

def test_get_customer_success():
    mock_session = MagicMock()
    mock_customer = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_customer
    result = get_customer(mock_session, 1)
    mock_session.query.return_value.filter.assert_called_once()
    assert result == mock_customer

def test_update_customer_success():
    mock_session = MagicMock()
    mock_customer = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_customer
    mock_update_data = MagicMock()
    mock_update_data.dict.return_value = {"last_name": "Doe"}
    mock_session.commit.return_value = None
    result = update_customer(mock_session, mock_update_data, 1)
    
    mock_session.query.return_value.filter.assert_called_once()
    assert result == mock_customer
    assert mock_customer.last_name == "Doe"
    mock_session.commit.assert_called_once()
def test_update_customer_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_update_data = MagicMock()
    mock_update_data.dict.return_value = {"last_name": "Doe"}
    result = update_customer(mock_session, mock_update_data, 1)
    assert result is None

def test_update_customer_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    mock_update_data = MagicMock()
    mock_update_data.dict.return_value = {"last_name": "Doe"}
    with pytest.raises(Exception):
        update_customer(mock_session, mock_update_data, 1)
        mock_session.commit.assert_not_called()
        
def test_delete_customer_success():
    mock_session = MagicMock()

    mock_customer = MagicMock()

    mock_session.query.return_value.filter.return_value.first.return_value = mock_customer

    result = delete_customer(mock_session, 1)

    mock_session.query.assert_called_once_with(Customers)
    mock_session.query.return_value.filter.assert_called_once()

    mock_session.delete.assert_called_once_with(mock_customer)
    mock_session.commit.assert_called_once()

    assert result is True

def test_delete_customer_fail():
    mock_session = MagicMock()

    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")

    with pytest.raises(Exception):
        delete_customer(mock_session, 1)