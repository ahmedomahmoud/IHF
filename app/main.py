from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
import schemas
import utils
import auth
import database
from fastapi.security import OAuth2PasswordRequestForm
from manage_data.parser import parse_cp_file
from manage_data.data_orm import Champ
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker   
from pprint import pprint
from datetime import date

app = FastAPI()

# pprint(parsed_data["gameinfo"])

load_dotenv()

# Build DATABASE_URL
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASS, DB_HOST, DB_NAME]):
    raise RuntimeError("Missing DB configuration in .env")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

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


# --- UPLOAD CP FILE ---
@app.post("/upload-cp-file/")
async def upload_cp_file(file: UploadFile = File(...)):
    file_content = await file.read()
    parsed_data = parse_cp_file(file_content)
    pprint(parsed_data["gameinfo"])
    session = SessionLocal()
    try:
        champ = Champ(name="World Handball Championship 2025", session=session)
        if not champ.champ_exists:
            champ.add_championship("World Handball Championship 2025", "The 29th edition of the championship.", date(2025, 1, 14), date(2025, 2, 2))
        print("Processing parsed data...")
        champ.process_data(parsed_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()
    





