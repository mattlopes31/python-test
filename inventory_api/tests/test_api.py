import pytest
from app.main import app, SERVERS


@pytest.fixture
def client():
    """Fixture pour créer un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test de l'endpoint health check"""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "OK"
    assert data["version"] == "1.0"


def test_list_servers(client):
    """Test de l'endpoint list_servers"""
    response = client.get('/api/v1/servers')
    assert response.status_code == 200
    data = response.get_json()
    assert "servers" in data
    assert "count" in data
    assert data["count"] == 2
    assert len(data["servers"]) == 2


def test_get_server_by_id_success(client):
    """Test de l'endpoint get_server avec un ID valide"""
    response = client.get('/api/v1/servers/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["hostname"] == "web-prod-01"
    assert data["ip"] == "10.0.0.1"
    assert data["status"] == "up"


def test_get_server_by_id_not_found(client):
    """Test de l'endpoint get_server avec un ID inexistant"""
    response = client.get('/api/v1/servers/999')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Server not found"


def test_get_server_by_id_second_server(client):
    """Test de l'endpoint get_server avec le deuxième serveur"""
    response = client.get('/api/v1/servers/2')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 2
    assert data["hostname"] == "db-prod-01"
    assert data["ip"] == "10.0.0.2"
    assert data["status"] == "down"
