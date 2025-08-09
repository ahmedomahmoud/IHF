from fastapi import FastAPI, HTTPException, Depends
import schemas
import utils
import auth
import database
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from typing import List

app = FastAPI()


# --- REGISTER ---
@app.post("/auth/register", status_code=201)
async def register(user: schemas.UserCreate):
    existing_user = await database.user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = utils.hash_password(user.password)

    new_user = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "password": hashed_pw
    }

    result = await database.user_collection.insert_one(new_user)

    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}


# --- LOGIN ---
@app.post("/auth/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await database.user_collection.find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not utils.verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = auth.create_access_token(data={"sub": user["username"]})

    return {"access_token": token, "token_type": "bearer"}




# --- GET All Championships (Public) ---
@app.get("/championships", response_model=List[schemas.ChampionshipOut])
async def get_all_championships():
    championships = []
    cursor = database.championship_collection.find()
    async for champ in cursor:
        champ["id"] = str(champ["_id"])
        championships.append(schemas.ChampionshipOut(**champ))
    return championships


# --- GET One Championship (Public) ---
@app.get("/championships/{champ_id}", response_model=schemas.ChampionshipOut)
async def get_championship(champ_id: str):
    champ = await database.championship_collection.find_one({"_id": ObjectId(champ_id)})
    if not champ:
        raise HTTPException(status_code=404, detail="Championship not found")
    champ["id"] = str(champ["_id"])
    return schemas.ChampionshipOut(**champ)


# --- CREATE Championship (Protected) ---
@app.post("/championships", response_model=schemas.ChampionshipOut)
async def create_championship(
    champ: schemas.ChampionshipCreate,
    current_user: schemas.UserOut = Depends(auth.get_current_user)
):
    new_champ = champ.dict()
    result = await database.championship_collection.insert_one(new_champ)
    new_champ["id"] = str(result.inserted_id)
    return schemas.ChampionshipOut(**new_champ)


# --- UPDATE Championship (Protected) ---
@app.put("/championships/{champ_id}", response_model=schemas.ChampionshipOut)
async def update_championship(
    champ_id: str,
    update: schemas.ChampionshipUpdate,
    current_user: schemas.UserOut = Depends(auth.get_current_user)
):
    updated_data = {k: v for k, v in update.dict().items() if v is not None}
    result = await database.championship_collection.update_one(
        {"_id": ObjectId(champ_id)},
        {"$set": updated_data}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Championship not found or no changes")

    champ = await database.championship_collection.find_one({"_id": ObjectId(champ_id)})
    champ["id"] = str(champ["_id"])
    return schemas.ChampionshipOut(**champ)


# --- DELETE Championship (Protected) ---
@app.delete("/championships/{champ_id}")
async def delete_championship(
    champ_id: str,
    current_user: schemas.UserOut = Depends(auth.get_current_user)
):
    result = await database.championship_collection.delete_one({"_id": ObjectId(champ_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Championship not found")
    return {"message": "Championship deleted successfully"}
