from sqlalchemy.orm import Session
from app.infra.db_models import LivreDB, ReservationDB, LecteurDB
from app.domain.models import QUOTA_MAX, StatutReservation
from datetime import datetime, timezone

class ErreurMetier(Exception):
    def __init__(self, message: str, code_http: int = 400):
        self.message = message
        self.code_http = code_http

def reserver_livre(db: Session, livre_id: int, lecteur_id: int):
    # 1. Vérifier si le lecteur existe
    lecteur = db.query(LecteurDB).filter(LecteurDB.id == lecteur_id).first()
    if not lecteur:
        raise ErreurMetier("Lecteur introuvable", 404)

    # 2. Vérifier le quota (max 3)
    reservations_actives = db.query(ReservationDB).filter(
        ReservationDB.lecteur_id == lecteur_id,
        ReservationDB.statut.in_([StatutReservation.RESERVEE.value, StatutReservation.EMPRUNTEE.value])
    ).count()
    if reservations_actives >= QUOTA_MAX:
        raise ErreurMetier("Quota dépassé : maximum 3 réservations actives.", 422)

    # 3. Créer la réservation
    try:
        nouvelle = ReservationDB(
            livre_id=livre_id, 
            lecteur_id=lecteur_id,
            date_creation=datetime.now(timezone.utc)
        )
        db.add(nouvelle)
        db.commit()
        db.refresh(nouvelle)
        return nouvelle
    except Exception as e:
        db.rollback()
        if "UNIQUE constraint failed" in str(e):
            raise ErreurMetier("Ce livre est déjà réservé.", 409)
        raise ErreurMetier("Erreur lors de la réservation.", 500)