
J'ai choisi **Python avec FastAPI** pour l'API, **SQLAlchemy** pour l'ORM et **SQLite** pour la base de données. Ce choix a été fait pour sa rapidité de mise en place et sa lisibilité. FastAPI génère automatiquement la documentation OpenAPI (Swagger) et permet de renvoyer facilement des codes HTTP précis (409, 422).


1. Créer un environnement virtuel : `python -m venv .venv`
2. L'activer : `source .venv/bin/activate` (ou `.venv\Scripts\activate` sur Windows)
3. Installer les dépendances : `pip install -r requirements.txt`


- Démarrer le serveur : `uvicorn app.http.main:app --reload`
- Initialiser la base de données de test : ouvrir `http://127.0.0.1:8000/init` dans le navigateur.
- Tester l'interface : `http://127.0.0.1:8000`
- Documentation Swagger : `http://127.0.0.1:8000/docs`

## Lancer les tests
```bash
pytest