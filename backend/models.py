from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ARCHITECT = "architect"
    PROMPT_ENGINEER = "prompt_engineer"


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    full_name: Optional[str] = None
    role: UserRole = Field(default=UserRole.ARCHITECT)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserRead(UserBase):
    id: int
    created_at: datetime


class PromptBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    template: str
    input_variables: str  # Comma-separated list of variables
    tags: Optional[str] = None
    model_config_json: Optional[str] = None  # JSON string for model params


class Prompt(PromptBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ChainBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    framework: str = Field(
        default="General", index=True
    )  # e.g., "4EM", "TOGAF", "ArchiMate", "Zachman"


class Chain(ChainBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    steps: List["ChainStep"] = Relationship(back_populates="chain")


class ChainStepBase(SQLModel):
    chain_id: int = Field(foreign_key="chain.id")
    prompt_id: int = Field(foreign_key="prompt.id")
    order: int
    input_mapping: Optional[str] = None  # JSON string mapping outputs to inputs
    is_critic: bool = Field(default=False)
    output_schema: Optional[str] = None  # Pydantic model name for validation


class ChainStep(ChainStepBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    chain: Chain = Relationship(back_populates="steps")
    prompt: Prompt = Relationship()


class ExecutionHistoryBase(SQLModel):
    prompt_id: int = Field(foreign_key="prompt.id")
    inputs: str  # JSON string of input values
    result: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ExecutionHistory(ExecutionHistoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prompt: Prompt = Relationship()


# Read Models for API responses (Nested)
class PromptRead(PromptBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ChainStepRead(ChainStepBase):
    id: int
    prompt: Optional[PromptRead] = None


class ChainRead(ChainBase):
    id: int
    created_at: datetime
    updated_at: datetime
    steps: List[ChainStepRead] = []


class ExecutionHistoryRead(ExecutionHistoryBase):
    id: int
    created_at: datetime
    prompt: Optional[PromptRead] = None


# Audit Log for Collaborative Activity
class AuditLogBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    action: str  # e.g., "Updated Prompt", "Created Chain", "Executed Model"
    target_type: str  # "prompt", "chain", "execution"
    target_id: int
    details: str


class AuditLog(AuditLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user: "User" = Relationship()


class AuditLogRead(AuditLogBase):
    id: int
    created_at: datetime
    user: Optional[UserRead] = None
