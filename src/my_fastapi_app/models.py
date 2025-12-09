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
    source_weights = relationship("SourceWeight", back_populates="operator")


class Lead(Base):
    __tablename__ = 'leads'
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"))
    operator = relationship("Operator", back_populates="leads")
    contacts = relationship("Contact", back_populates="lead")


class Source(Base):
    __tablename__= 'sources'
    name = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)
    operator_weights = relationship("SourceWeight", back_populates="source")


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"))

    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source")
    operator = relationship("Operator")


class SourceWeight(Base):
    __tablename__ = 'source_weights'
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"))
    weight = Column(Integer)

    source = relationship("Source", back_populates="operator_weights")
    operator = relationship("Operator", back_populates="source_weights")




