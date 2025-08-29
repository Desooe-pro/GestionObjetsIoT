# Import
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import os
from pymongo import MongoClient
from dotenv import load_dotenv
# Chargement du fichier .env
load_dotenv()

URL = os.getenv('DB_URL')

app = FastAPI()

# Route de test
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Je récupère la base de données
def get_database():
    client = MongoClient(URL, tls=True, tlsAllowInvalidCertificates=True)
    return client["mqtt"]




templates = Jinja2Templates(directory="templates")

@app.get("/info")
async def get_all_mqtt(request: Request):
    db = get_database()
    collection = db["mqtt"]

    # Récupère les données triées par date
    infos = list(collection.find().sort([("received_at", 1)]))

    # Convertit les ObjectId en str pour Jinja2
    for info in infos:
        info["_id"] = str(info["_id"])

    return templates.TemplateResponse(
        "infos.html",
        {"request": request, "infos": infos}
    )