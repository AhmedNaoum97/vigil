from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from models.database import Base


class ScanStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class Protocol(str, enum.Enum):
    tcp = "tcp"
    udp = "udp"


class Severity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    scan_jobs = relationship("ScanJob", back_populates="user")


class ScanJob(Base):
    __tablename__ = "scan_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target = Column(String, nullable=False)
    status = Column(Enum(ScanStatus), default=ScanStatus.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="scan_jobs")
    results = relationship("ScanResult", back_populates="scan_job")


class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    scan_job_id = Column(Integer, ForeignKey("scan_jobs.id"), nullable=False)
    host = Column(String, nullable=True)
    port = Column(Integer, nullable=False)
    protocol = Column(Enum(Protocol), nullable=False)
    service_name = Column(String, nullable=True)
    service_version = Column(String, nullable=True)

    scan_job = relationship("ScanJob", back_populates="results")
    findings = relationship("Finding", back_populates="scan_result")


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    scan_result_id = Column(Integer, ForeignKey("scan_results.id"), nullable=False)
    cve_id = Column(String, nullable=False)
    severity = Column(Enum(Severity), nullable=False)
    description = Column(String, nullable=True)
    source = Column(String, nullable=True)

    scan_result = relationship("ScanResult", back_populates="findings")