from fastapi.testclient import TestClient
from app.http.main import app
from app.infra.database import SessionLocal, engine, Base
from app.infra.db_models import LivreDB, LecteurDB
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # On crée une base propre avant chaque test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add(LivreDB(id=1, titre="Harry Potter", auteur="Rowling", annee=1997))
    db.add(LecteurDB(id=1, nom="Alice", email="alice@test.com"))
    db.add(LecteurDB(id=2, nom="Bob", email="bob@test.com"))
    db.commit()
    db.close()

def test_reservation_nominale():
    response = client.post("/reservations", json={"livre_id": 1, "lecteur_id": 1})
    assert response.status_code == 201

def test_double_reservation_echoue():
    # Alice réserve
    client.post("/reservations", json={"livre_id": 1, "lecteur_id": 1})
    # Bob essaie de réserver le même livre
    response = client.post("/reservations", json={"livre_id": 1, "lecteur_id": 2})
    assert response.status_code == 409
    assert "déjà réservé" in response.json()["detail"]