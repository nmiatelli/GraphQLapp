from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship 

# Módulo que nos permite criar tabelas de forma declarativa
Base = declarative_base()

# Tabela
class Employer(Base):
    __tablename__ = "employers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    contact_email = Column(String)
    industry = Column(String)
    jobs = relationship("Job", back_populates="employer", lazy="joined")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    
    employer = relationship("Employer", back_populates="jobs", lazy="joined")
    applications = relationship("JobApplication", back_populates="job", lazy="joined")

class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(String)
    # employer_id = Column(Integer, ForeignKey("employers.id"))

    applications = relationship("JobApplication", back_populates="user", lazy="joined")


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    # definindo relações
    user = relationship("User", back_populates="applications", lazy="joined")
    job = relationship("Job", back_populates="applications", lazy="joined")

