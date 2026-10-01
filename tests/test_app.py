import pytest
from src.app import app, validate_application_data

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_successful_application_validation():
    """1-тест: Дұрыс мәліметтер кезіндегі валидация нәтижесі"""
    valid_data = {
        "full_name": "Асқар Нұрланұлы",
        "faculty": "Ақпараттық технологиялар",
        "gpa": 3.67
    }
    is_valid, msg = validate_application_data(valid_data)
    assert is_valid is True
    assert msg == "Деректер дұрыс"

def test_invalid_gpa_validation():
    """2-тест: Қате GPA кезінде валидациядан өтпеуін тексеру"""
    invalid_data = {
        "full_name": "Серік Ахмет",
        "faculty": "Инженерия",
        "gpa": 4.5  
    }
    is_valid, msg = validate_application_data(invalid_data)
    assert is_valid is False
    assert "GPA 0.0 мен 4.0 аралығында" in msg

def test_api_post_application(client):
    """Қосымша тест: API эндпоинты арқылы өтінім жіберу"""
    response = client.post("/applications", json={
        "full_name": "Айша Бақытқызы",
        "faculty": "Экономика",
        "gpa": 3.2
    })
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["application"]["status"] == "Submitted"