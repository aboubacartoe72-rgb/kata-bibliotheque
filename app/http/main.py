from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.infra.database import engine, Base, get_db
from app.infra.db_models import LivreDB
from app.application.use_cases import reserver_livre, ErreurMetier

# Création de la table au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bibliothèque API")
templates = Jinja2Templates(directory="app/templates")

class LivreCreate(BaseModel):
    titre: str
    auteur: str
    annee: int

class ReservationCreate(BaseModel):
    livre_id: int
    lecteur_id: int

@app.get("/", response_class=HTMLResponse)
def accueil(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/livres", status_code=201)
def creer_livre(livre: LivreCreate, db: Session = Depends(get_db)):
    nouveau = LivreDB(**livre.model_dump())
    db.add(nouveau)
    db.commit()
    db.refresh(nouveau)
    return nouveau

@app.get("/livres")
def lister_livres(db: Session = Depends(get_db)):
    return db.query(LivreDB).all()

# C'EST CETTE ROUTE QUI MANQUAIT !
@app.post("/reservations", status_code=201)
def creer_reservation(res: ReservationCreate, db: Session = Depends(get_db)):
    try:
        return reserver_livre(db, res.livre_id, res.lecteur_id)
    except ErreurMetier as e:
        raise HTTPException(status_code=e.code_http, detail=e.message)