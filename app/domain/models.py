from datetime import datetime, timedelta
from enum import Enum

class StatutReservation(str, Enum):
    RESERVEE = "RESERVEE"
    EMPRUNTEE = "EMPRUNTEE"

QUOTA_MAX = 3
DUREE_EXPIRATION = timedelta(hours=48)

def est_expiree(date_reservation: datetime, maintenant: datetime) -> bool:
    return (maintenant - date_reservation) > DUREE_EXPIRATION

def est_livre_disponible(reservations_du_livre: list) -> bool:
    for r in reservations_du_livre:
        if r.statut in [StatutReservation.RESERVEE, StatutReservation.EMPRUNTEE]:
            return False
    return True