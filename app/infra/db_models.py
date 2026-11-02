from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.infra.database import Base
from app.domain.models import StatutReservation

class LivreDB(Base):
    __tablename__ = "livres"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, index=True)
    auteur = Column(String, index=True)
    annee = Column(Integer)
    # PAS DE COLONNE "DISPONIBLE" ICI ! C'est ça qui causait le bug.
    reservations = relationship("ReservationDB", back_populates="livre")

class LecteurDB(Base):
    __tablename__ = "lecteurs"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    email = Column(String, unique=True, index=True) # Email unique
    reservations = relationship("ReservationDB", back_populates="lecteur")

class ReservationDB(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    livre_id = Column(Integer, ForeignKey("livres.id"))
    lecteur_id = Column(Integer, ForeignKey("lecteurs.id"))
    statut = Column(String, default=StatutReservation.RESERVEE.value)
    date_creation = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    livre = relationship("LivreDB", back_populates="reservations")
    lecteur = relationship("LecteurDB", back_populates="reservations")

# LA CORRECTION ULTIME DU BUG :
# La base de données elle-même interdit d'avoir 2 réservations actives sur le même livre.
# Même si deux personnes cliquent en même temps, SQL fera une erreur.
Index('unique_livre_reserve', ReservationDB.livre_id, unique=True, 
      sqlite_where=ReservationDB.statut.in_([StatutReservation.RESERVEE.value, StatutReservation.EMPRUNTEE.value]))