from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from database import get_session
from models import Prompt

router = APIRouter(
    prefix="/prompts",
    tags=["prompts"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Prompt)
def create_prompt(prompt: Prompt, session: Session = Depends(get_session)):
    session.add(prompt)
    session.commit()
    session.refresh(prompt)
    return prompt

@router.get("/", response_model=List[Prompt])
def read_prompts(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    prompts = session.exec(select(Prompt).offset(skip).limit(limit)).all()
    return prompts

@router.get("/{prompt_id}", response_model=Prompt)
def read_prompt(prompt_id: int, session: Session = Depends(get_session)):
    prompt = session.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.delete("/{prompt_id}")
def delete_prompt(prompt_id: int, session: Session = Depends(get_session)):
    prompt = session.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    session.delete(prompt)
    session.commit()
    return {"ok": True}

@router.put("/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: int, prompt_data: Prompt, session: Session = Depends(get_session)):
    prompt = session.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    prompt_data_dict = prompt_data.dict(exclude_unset=True)
    for key, value in prompt_data_dict.items():
        setattr(prompt, key, value)
        
    session.add(prompt)
    session.commit()
    session.refresh(prompt)
    return prompt
