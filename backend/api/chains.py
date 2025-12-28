from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from database import get_session
from models import Chain

router = APIRouter(
    prefix="/chains",
    tags=["chains"],
    responses={404: {"description": "Not found"}},
)

from models import Chain, ChainStep

@router.post("/", response_model=Chain)
def create_chain(chain: Chain, session: Session = Depends(get_session)):
    # Note: This simple create doesn't handle nested steps creation automatically unless we use a Pydantic model with steps
    # For simplicity, we'll assume the client sends the chain info first, then adds steps, OR we accept a complex object.
    # Let's keep it simple: Create Chain first.
    session.add(chain)
    session.commit()
    session.refresh(chain)
    return chain

@router.post("/{chain_id}/steps", response_model=ChainStep)
def add_step(chain_id: int, step: ChainStep, session: Session = Depends(get_session)):
    step.chain_id = chain_id
    session.add(step)
    session.commit()
    session.refresh(step)
    return step

@router.get("/", response_model=List[Chain])
def read_chains(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    chains = session.exec(select(Chain).offset(skip).limit(limit)).all()
    return chains

@router.get("/{chain_id}", response_model=Chain)
def read_chain(chain_id: int, session: Session = Depends(get_session)):
    chain = session.get(Chain, chain_id)
    if not chain:
        raise HTTPException(status_code=404, detail="Chain not found")
    return chain

@router.delete("/{chain_id}")
def delete_chain(chain_id: int, session: Session = Depends(get_session)):
    chain = session.get(Chain, chain_id)
    if not chain:
        raise HTTPException(status_code=404, detail="Chain not found")
    session.delete(chain)
    session.commit()
    return {"ok": True}
