from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class PromptBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    template: str
    input_variables: str  # Comma-separated list of variables
    tags: Optional[str] = None
    model_config_json: Optional[str] = None # JSON string for model params

class Prompt(PromptBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ChainBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None

class Chain(ChainBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    steps: List["ChainStep"] = Relationship(back_populates="chain")

class ChainStepBase(SQLModel):
    chain_id: int = Field(foreign_key="chain.id")
    prompt_id: int = Field(foreign_key="prompt.id")
    order: int
    input_mapping: Optional[str] = None # JSON string mapping outputs to inputs

class ChainStep(ChainStepBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    chain: Chain = Relationship(back_populates="steps")
    prompt: Prompt = Relationship()
