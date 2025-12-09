from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship

from src.my_fastapi_app.database import Base


class Operator(Base):
    __tablename__='operators'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer,prymary_key=True, index=True)
    is_active = Column(Boolean, defalt=True)
    max_active_lead = Column(Integer, default=5)
    weight = Column(Integer, default=1)

    leads = relationship("Lead", back_populates="operator")


class Lead(Base):
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)


