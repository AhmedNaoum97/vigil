import ipaddress
from pydantic import field_validator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from models.database import get_db
from models.models import User, ScanJob
from api.auth import hash_password, verify_password, create_access_token, get_current_user

app = FastAPI(title="Vigil")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ScanRequest(BaseModel):
    target: str

    @field_validator("target")
    @classmethod
    def target_must_be_private_ip(cls, value: str) -> str:
        try:
            ip = ipaddress.ip_address(value)
        except ValueError:
            raise ValueError("Target must be a valid IP address")
        if not ip.is_private:
            raise ValueError("Only private (lab) IP addresses are allowed")
        return value


@app.get("/")
def root():
    return {"status": "Vigil API is running"}


@app.post("/auth/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "email": new_user.email}


@app.post("/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}

@app.post("/scans")
def create_scan(
    payload: ScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = ScanJob(user_id=current_user.id, target=payload.target)
    db.add(job)
    db.commit()
    db.refresh(job)
    return {"job_id": job.id, "status": job.status}

@app.get("/scans")
def list_scans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    jobs = (
        db.query(ScanJob)
        .filter(ScanJob.user_id == current_user.id)
        .order_by(ScanJob.created_at.desc())
        .all()
    )
    return [
        {"job_id": job.id, "target": job.target, "status": job.status, "created_at": job.created_at}
        for job in jobs
    ]


@app.get("/scans/{job_id}")
def get_scan(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = (
        db.query(ScanJob)
        .filter(ScanJob.id == job_id, ScanJob.user_id == current_user.id)
        .first()
    )
    if not job:
        raise HTTPException(status_code=404, detail="Scan not found")

    return {
        "job_id": job.id,
        "target": job.target,
        "status": job.status,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
    }