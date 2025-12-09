from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Operator, Source, Contact, Lead
from .schemas import OperatorCreate, SourceCreate, ContactCreate, OperatorResponse, SourceResponse, ContactResponse
from .services import create_contact

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/operators", response_model=OperatorResponse)
def create_operator(operator: OperatorCreate, db: Session = Depends(get_db)):
    db_operator = Operator(**operator.dict())
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator

@app.get("/operators", response_model=list[OperatorResponse])
def get_operators(db: Session = Depends(get_db)):
    return db.query(Operator).all()

@app.put("/operators/{operator_id}", response_model=OperatorResponse)
def update_operator(operator_id: int, operator: OperatorCreate, db: Session = Depends(get_db)):
    db_operator = db.query(Operator).filter(Operator.id == operator_id).first()
    for key, value in operator.dict().items():
        setattr(db_operator, key, value)
    db.commit()
    return db_operator


@app.post("/sources", response_model=SourceResponse)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    db_source = Source(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


@app.post("/contacts", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db=db, external_id=contact.external_id, source_id=contact.source_id)


@app.get("/leads")
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).all()
