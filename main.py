# ===== MUST BE FIRST =====
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

# ❌ REMOVE sys.path hacks (not needed on Vercel)
# import sys
# from pathlib import Path
# sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import get_db
from py_models.signin_models import User
from py_models.course_models import Course
from py_models.quiz_models import Quiz
from py_models.enrollment_models import Enrollment

from py_schemas.signin_schemas import CreateUser
from py_schemas.course_schemas import Create_course
from py_schemas.quizz_schemas import CreateQuiz
from py_schemas.enrollment_schemas import (
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
)

app = FastAPI(title="SkillNest API", version="1.0.0")

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # OK for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ROOT HEALTH CHECK (IMPORTANT FOR VERCEL) =====
@app.get("/")
def health_check():
    return {"message": "SkillNest FastAPI running"}

# ================= USER APIs =================

@app.get("/users")
def get_all_user(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/user/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/create_user")
def add_user(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.user_email == user.user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User added successfully"}

@app.post("/login")
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.user_email == data.get("email"),
        User.user_password == data.get("password")
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": user.user_id,
        "user_name": user.user_name
    }

# ================= COURSE APIs =================

@app.post("/create_course")
def create_course(course: Create_course, db: Session = Depends(get_db)):
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"message": "Course added successfully"}

@app.get("/course")
def get_all_course(db: Session = Depends(get_db)):
    return db.query(Course).all()

# ================= ENROLLMENT =================

@app.post("/enroll")
def enroll_course(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == enrollment.user_id,
        Enrollment.course_name == enrollment.course_name
    ).first()

    if existing:
        return {"message": "Already enrolled"}

    new_enrollment = Enrollment(
        user_id=enrollment.user_id,
        course_name=enrollment.course_name,
        video_progress=0,
        is_completed=False,
        learning_hours=0.0
    )

    db.add(new_enrollment)
    db.commit()
    return {"message": "Enrolled successfully"}

@app.get("/mylearning/{user_id}")
def get_my_learning(user_id: int, db: Session = Depends(get_db)):
    return db.query(Enrollment).filter(Enrollment.user_id == user_id).all()

# ================= QUIZ =================

@app.post("/create_quiz")
def create_quiz(data: CreateQuiz, db: Session = Depends(get_db)):
    quiz = Quiz(**data.dict())
    db.add(quiz)
    db.commit()
    return {"message": "Quiz added successfully"}

@app.get("/quiz_score/{user_id}/{course_name}")
def get_quiz_score(user_id: int, course_name: str, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(
        Quiz.user_id == user_id,
        Quiz.course_name == course_name
    ).order_by(Quiz.score.desc()).first()

    if not quiz:
        return {"course_name": course_name, "score": 0}

    return quiz
