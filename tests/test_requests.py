import uuid

import pytest
from unittest.mock import MagicMock
from models.models import Customers
from repositories.requests_repo import (create_request, delete_request, get_request, update_request, get_all_requests)

def test_create_form_request_success():
    mock_session = MagicMock()
    mock_form_request = MagicMock()
    mock_form_request.dict.return_value = {
    "requested_by": uuid.uuid4(),
    "request_data": {"type": "A"},
    "reason": "Some details"
}
    create_request(mock_session, mock_form_request)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_form_request_fail():
    mock_session = MagicMock()
    mock_form_request = MagicMock()
    mock_form_request.dict.return_value = {
        "requested_by": uuid.uuid4(),
        "request_data": {"type": "A"},
        "reason": "Some details"
    }
    mock_session.commit.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        create_request(mock_session, mock_form_request)

def test_get_form_request_success():
    mock_session = MagicMock()
    mock_form_request = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_form_request
    result = get_request(mock_session, 1)
    mock_session.query.return_value.filter.assert_called_once()
    assert result == mock_form_request

def test_get_form_request_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    result = get_request(mock_session, 1)
    mock_session.query.return_value.filter.assert_called_once()
    assert result is None

def test_get_form_request_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        get_request(mock_session, 1)

def test_update_form_request_success():
    mock_session = MagicMock()
    mock_form_request = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_form_request
    mock_update_data = MagicMock()
    mock_update_data.dict.return_value = {"reason": "Updated reason"}
    mock_session.commit.return_value = None
    result = update_request(mock_session, mock_update_data, 1)
    
    mock_session.query.return_value.filter.assert_called_once()
    assert result == mock_form_request
    assert mock_form_request.reason == "Updated reason"
    mock_session.commit.assert_called_once()

def test_update_form_request_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_update_data = MagicMock()
    mock_update_data.dict.return_value = {"reason": "Updated reason"}
    result = update_request(mock_session, mock_update_data, 1)
    assert result is None
    
def test_update_form_request_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    mock_update_data = MagicMock()
    mock_update_data.dict.return_value = {"reason": "Updated reason"}
    with pytest.raises(Exception):
        update_request(mock_session, mock_update_data, 1)
        mock_session.commit.assert_not_called()
    
def test_get_all_form_requests_success():
    mock_session = MagicMock()
    mock_form_requests = [MagicMock(), MagicMock()]
    mock_session.query.return_value.all.return_value = mock_form_requests
    result = get_all_requests(mock_session)
    mock_session.query.return_value.all.assert_called_once()
    assert result == mock_form_requests

def test_get_all_form_requests_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.all.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        get_all_requests(mock_session)
        
def test_delete_form_request_success():
    mock_session = MagicMock()
    mock_form_request = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_form_request
    result = delete_request(mock_session, 1)
    mock_session.query.return_value.filter.assert_called_once()
    assert result is True
    mock_session.delete.assert_called_once_with(mock_form_request)
    mock_session.commit.assert_called_once()

def test_delete_form_request_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    result = delete_request(mock_session, 1)
    mock_session.query.return_value.filter.assert_called_once()
    assert result is False

def test_delete_form_request_fail():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        delete_request(mock_session, 1)
        mock_session.commit.assert_not_called()

