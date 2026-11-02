from django.db import models

# Create your models here.
from datetime import datetime, timedelta
from enum import Enum

class StatutReservation(str, Enum):
    RESERVEE = "RESERVEE"
    EMPRUNTEE = "EMPRUNTEE"
    RETOURNEE = "RETOURNEE"
    ANNULEE = "ANNULEE"
    EXPIREE = "EXPIREE"

# Règle du quota
QUOTA_MAX = 3
# Règle de l'expiration (48h)
DUREE_EXPIRATION = timedelta(hours=48)

def est_expiree(date_reservation: datetime, maintenant: datetime) -> bool:
    return (maintenant - date_reservation) > DUREE_EXPIRATION

# C'EST ICI QU'ON CORRIGE LE BUG DE L'ÉNONCÉ :
# On ne stocke pas "disponible = faux". Un livre est indisponible 
# SI ET SEULEMENT SI il a une réservation avec le statut RESERVEE ou EMPRUNTEE.
def est_livre_disponible(reservations_du_livre: list) -> bool:
    for r in reservations_du_livre:
        if r.statut in [StatutReservation.RESERVEE, StatutReservation.EMPRUNTEE]:
            return False
    return True