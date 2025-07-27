from app import app, db
import os


with app.app_context():
    db.create_all()
    print("✅ Base de données créée avec succès !")
