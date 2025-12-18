from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import sys
from pathlib import Path

# Ensure project root is on sys.path so sibling packages can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import engine, get_db, Base
from py_models.signin_models import User
from py_models.course_models import Course
from py_models.quiz_models import Quiz
from py_models.enrollment_models import Enrollment

from py_schemas.signin_schemas import CreateUser
from py_schemas.course_schemas import Create_course
from py_schemas.quizz_schemas import CreateQuiz
from py_schemas.enrollment_schemas import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def get_all_user(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/user/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.user_id == id).first()

@app.post("/create_user")
def add_user(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.user_email == user.user_email).first()
    if existing_user:
         raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        user_name=user.user_name,
        user_email=user.user_email,
        user_password=user.user_password,
        user_dateofbirth=user.user_dateofbirth,
        user_phone=user.user_phone,
        user_gender=user.user_gender
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "user added successfully"

@app.post("/login")
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")
    user = db.query(User).filter(
        User.user_email == email,
        User.user_password == password
    ).first()
    if user:
        return {"message": "Login successful", "user_id": user.user_id, "user_name": user.user_name}
    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get("/login/{user_name}/{user_password}")
def login_old(user_name: str, user_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.user_name == user_name,
        User.user_password == user_password
    ).first()
    if user:
        return "Login successful"
    return "Invalid username or password"

@app.put("/user/{user_id}")
def update_user(user_id: int, data: dict = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    

    if "user_name" in data: user.user_name = data["user_name"]
    if "user_email" in data: user.user_email = data["user_email"]
    if "user_dateofbirth" in data: user.user_dateofbirth = data["user_dateofbirth"]
    if "user_phone" in data: user.user_phone = data["user_phone"]
    if "user_gender" in data: user.user_gender = data["user_gender"]
    if "password" in data and data["password"]: user.user_password = data["password"] 
    db.commit()
    return {"message": "Profile updated successfully"}

@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.post("/verify_user")
def verify_user(data: dict = Body(...), db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")
    user = db.query(User).filter(User.user_email == email, User.user_password == password).first()
    if user:
        return {"valid": True, "user_id": user.user_id}
    return {"valid": False}


@app.post("/create_course")
def create_course(course: Create_course, db: Session = Depends(get_db)):
    new_course = Course(
        course_id=course.course_id,
        title=course.title,
        description=course.description,
        category=course.category,
        level=course.level,
        created_by=course.created_by,  
        created_at=course.created_at
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return "course added successfully"

@app.get("/course")
def get_all_course(db: Session = Depends(get_db)):
    return db.query(Course).all()

@app.post("/enroll")
def enroll_course(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == enrollment.user_id, 
        Enrollment.course_name == enrollment.course_name
    ).first()
    if not existing:
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

@app.put("/update_progress")
def update_progress(data: EnrollmentUpdate, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == data.user_id,
        Enrollment.course_name == data.course_name
    ).first()
    
    if not enrollment:
        enrollment = Enrollment(
            user_id=data.user_id,
            course_name=data.course_name,
            video_progress=data.video_progress,
            is_completed=data.is_completed,
            learning_hours=data.learning_hours
        )
        db.add(enrollment)
    else:
        enrollment.video_progress = data.video_progress
        if data.is_completed:
            enrollment.is_completed = True
        enrollment.learning_hours = data.learning_hours
        
    db.commit()
    return {"message": "Progress updated"}

@app.get("/mylearning/{user_id}")
def get_my_learning(user_id: int, db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user_id).all()
    return enrollments

@app.get("/dashboard_stats/{user_id}")
def get_dashboard_stats(user_id: int, db: Session = Depends(get_db)):
    completed_count = db.query(Enrollment).filter(
        Enrollment.user_id == user_id, 
        Enrollment.is_completed == True
    ).count()
    
    total_courses = 8 
    progress_percentage = (completed_count / total_courses) * 100
    return {"completed_count": completed_count, "total_courses": total_courses, "progress_percentage": progress_percentage}


@app.post("/create_quiz")
def create_quiz(data: CreateQuiz, db: Session = Depends(get_db)):
    new_quiz = Quiz(
        result_id=data.result_id,
        quiz_id=data.quiz_id,
        user_id=data.user_id,
        score=data.score,
        attempt_date=data.attempt_date
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return "quiz added successfully"
