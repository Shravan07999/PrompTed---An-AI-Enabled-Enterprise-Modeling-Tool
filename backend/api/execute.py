from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
from sqlmodel import Session
from database import get_session
from models import Prompt

router = APIRouter(
    prefix="/execute",
    tags=["execute"],
)

class ExecutionRequest(BaseModel):
    prompt_id: int
    inputs: Dict[str, Any]

@router.post("/")
def execute_prompt(request: ExecutionRequest, session: Session = Depends(get_session)):
    prompt = session.get(Prompt, request.prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Simulate LLM execution
    # In a real app, we would use LangChain or OpenAI client here.
    # For now, we just fill in the template.
    
    filled_template = prompt.template
    for key, value in request.inputs.items():
        filled_template = filled_template.replace(f"{{{{{key}}}}}", str(value))
        
    # Mock response
    result = f"[MOCK LLM OUTPUT] Based on your input, here is the result for '{prompt.name}':\n\n{filled_template}\n\n(This is a simulation. Configure an LLM provider to get real results.)"
    
    return {"result": result, "inputs": request.inputs, "filled_prompt": filled_template}
