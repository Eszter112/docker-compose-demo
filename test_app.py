import pytest
from app import app

@pytest.fixture 
def client():
    """Créer un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test de la route /"""
    response = client.get('/') 
    """Simule une vraie requête GET, mais sans lancer le serveur Flask. C'est du test unitaire"""
    assert response.status_code == 200
    assert b"Hello from Flask!" in response.data

def test_write(client):
    """Test de la route /write"""
    response = client.get('/write?msg=Test')
    assert response.status_code == 200
    assert b"Message" in response.data

def test_read(client):
    response = client.get('/read')
    assert response.status_code==200
    assert b"Message" or "aucun message" in response.data