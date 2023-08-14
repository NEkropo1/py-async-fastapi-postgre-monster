import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.responses import Response
from firebase_admin import credentials, firestore
from sqlalchemy.ext.asyncio import AsyncSession
from google.cloud.firestore import ArrayUnion

import firebase_admin
import crud
import models
from db.engine import AsyncSessionLocal

load_dotenv()
app = FastAPI()

API_KEY = os.getenv("API_KEY")

CURRENT_FILE_LOCATION = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(CURRENT_FILE_LOCATION, "antycode-3f8e262dd0a7.json"))
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key


@app.post("/store_json/")
async def store_json_endpoint(payload: models.JsonInput, db: AsyncSession = Depends(get_db), api_key: str = Depends(verify_api_key)):
    stored_data = await crud.create_json(db, payload.data)
    return {"message": "Data stored successfully", "stored_data_id": stored_data.id}


@app.post("/{server_id}/{thread_id}/")
async def push_data_to_firebase(data: dict, api_key: str = Depends(verify_api_key)):
    if not data:
        data = {}
    doc_id = data.get("id")

    if not doc_id:
        raise HTTPException(status_code=400, detail="Missing 'id' field in data.")

    doc_ref = firestore_db.collection("accounts").document(str(doc_id))

    try:
        doc_ref.update({
            "registration_results": ArrayUnion([data])
        })
        return {"message": "Data appended successfully"}
    except Exception as e:
        if "NOT_FOUND" in str(e):
            doc_ref.set({
                "registration_results": [data]
            })
            return {"message": "Document created and data appended successfully"}
        else:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/{server_id}/{thread_id}/")
async def get_next_available_json(server_id: int, thread_id: int, db: AsyncSession = Depends(get_db), api_key: str = Depends(verify_api_key)):
    json_data = await crud.get_next_unlocked_json(db)
    if not json_data:
        return Response(status_code=204)
    return json_data
