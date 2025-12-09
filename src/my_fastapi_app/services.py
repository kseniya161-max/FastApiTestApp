from sqlalchemy.orm import Session
import random
from .models import Lead, Operator, SourceWeight, Contact


def create_contact(db: Session, external_id: str, source_id: int):
    lead = db.query(Lead).filter(Lead.external_id == external_id).first()
    if not lead:
        lead = Lead(external_id=external_id)
        db.add(lead)
        db.commit()
        db.refresh(lead)

    available_operators = (
        db.query(Operator)
        .join(SourceWeight)
        .filter(SourceWeight.source_id == source_id)
        .filter(Operator.is_active == True)
        .all()
    )

    available_operators = [
        op for op in available_operators if len(op.leads) < op.max_active_leads
    ]

    if not available_operators:
        return {"message": "Нет Доступных операторов", "lead_id": lead.id}


    total_weight = sum(source_weight.weight for op in available_operators for source_weight in op.operator_weights if
                       source_weight.source_id == source_id)

    if total_weight == 0:
        return {"message": "No weights defined for available operators", "lead_id": lead.id}

    random_choice = random.randint(1, total_weight)
    cumulative_weight = 0
    selected_operator = None

    for operator in available_operators:
        cumulative_weight += operator.weight
        if random_choice <= cumulative_weight:
            selected_operator = operator
            break

    contact = Contact(lead_id=lead.id, source_id=source_id, operator_id=selected_operator.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return {
        "contact_id": contact.id,
        "lead_id": lead.id,
        "operator_id": selected_operator.id
    }
