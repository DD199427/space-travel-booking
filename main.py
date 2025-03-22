from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

USERS_FILE = "users.json"
BOOKINGS_FILE = "bookings.json"

# Ensure JSON files exist
for file in [USERS_FILE, BOOKINGS_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)


# 🚀 Authentication Model
class User(BaseModel):
    username: str
    password: str


# 🚀 Booking Model
class Booking(BaseModel):
    username: str
    destination: str
    travel_class: str


# 🚀 Sign Up
@app.post("/signup")
def signup(user: User):
    with open(USERS_FILE, "r+") as file:
        users = json.load(file)
        if user.username in users:
            raise HTTPException(status_code=400, detail="User already exists!")
        users[user.username] = user.password
        file.seek(0)
        json.dump(users, file)
    return {"message": "User registered successfully!"}


# 🚀 Sign In
@app.post("/signin")
def signin(user: User):
    with open(USERS_FILE, "r") as file:
        users = json.load(file)
        if users.get(user.username) != user.password:
            raise HTTPException(status_code=401, detail="Invalid credentials!")
    return {"message": "Login successful!"}


# 🚀 Book a Space Voyage
@app.post("/book")
def book_trip(booking: Booking):
    available_classes = ["Luxury", "Deluxe", "VIP Zero Gravity", "Economy"]
    available_destinations = ["Lunar Hotel", "Space Station"]

    if booking.travel_class not in available_classes:
        raise HTTPException(status_code=400, detail="Invalid travel class!")
    
    if booking.destination not in available_destinations:
        raise HTTPException(status_code=400, detail="Invalid destination!")

    with open(BOOKINGS_FILE, "r+") as file:
        bookings = json.load(file)
        if booking.username not in bookings:
            bookings[booking.username] = []
        bookings[booking.username].append({
            "destination": booking.destination,
            "travel_class": booking.travel_class
        })
        file.seek(0)
        json.dump(bookings, file)

    return {"message": "Booking successful!"}
