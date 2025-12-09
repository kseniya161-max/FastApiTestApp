from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from src.my_fastapi_app.database import Base


class Operator(Base):
    __tablename__='operators'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    max_active_leads = Column(Integer, default=5)
    weight = Column(Integer, default=1)

    leads = relationship("Lead", back_populates="operator")


class Lead(Base):
    __tablename__ = 'leads'
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"))
    operator = relationship("Operator", back_populates="leads")


