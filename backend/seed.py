from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import User, UserRole, Prompt, Chain, ChainStep, ExecutionHistory, AuditLog


def seed():
    create_db_and_tables()

    with Session(engine) as session:
        # 1. USERS
        admin = session.exec(select(User).where(User.username == "engineer")).first()
        if not admin:
            admin = User(
                username="engineer",
                full_name="Edward Engineer",
                role=UserRole.PROMPT_ENGINEER,
                hashed_password="hashed_password_placeholder_123",
            )
            session.add(admin)

        architect = session.exec(
            select(User).where(User.username == "architect")
        ).first()
        if not architect:
            architect = User(
                username="architect",
                full_name="Alice Architect",
                role=UserRole.ARCHITECT,
                hashed_password="hashed_password_placeholder_456",
            )
            session.add(architect)

        session.commit()
        session.refresh(admin)
        session.refresh(architect)

        # 2. PROMPTS
        all_prompts = [
            # GREENSHARE
            Prompt(
                name="Greenshare: Sustainability Link",
                description="Strategy for asset sharing.",
                template="How does sharing {{equipment}} help ESG?",
                input_variables="equipment",
                tags="4EM, Strategy",
            ),
            Prompt(
                name="Greenshare: Technical Inventory",
                description="Hardware specs for sharing.",
                template="List sensors for {{equipment}}.",
                input_variables="equipment",
                tags="4EM, Technical",
            ),
            Prompt(
                name="Greenshare: Rental Governance",
                description="Rules for asset sharing.",
                template="Rules for renting {{equipment}}?",
                input_variables="equipment",
                tags="4EM, Governance",
            ),
            Prompt(
                name="Greenshare: Fulfillment Workflow",
                description="The process flow.",
                template="Steps to rent {{equipment}}?",
                input_variables="equipment",
                tags="4EM, Process",
            ),
            # URBANMICROGRID
            Prompt(
                name="UrbanMicroGrid: Revenue & ESG Strategy",
                description="Microgrid strategy.",
                template="Profit vs ESG for {{neighborhood_name}}.",
                input_variables="neighborhood_name",
                tags="4EM, Strategy",
            ),
            Prompt(
                name="UrbanMicroGrid: Smart Grid Specs",
                description="Microgrid hardware.",
                template="Hardware for {{neighborhood_name}}?",
                input_variables="neighborhood_name",
                tags="4EM, Technical",
            ),
            Prompt(
                name="UrbanMicroGrid: Trading Governance",
                description="Energy rules.",
                template="Pricing for {{neighborhood_name}}.",
                input_variables="neighborhood_name",
                tags="4EM, Governance",
            ),
            Prompt(
                name="UrbanMicroGrid: Fulfillment Workflow",
                description="Trading process.",
                template="How to trade in {{neighborhood_name}}?",
                input_variables="neighborhood_name",
                tags="4EM, Process",
            ),
        ]

        for p in all_prompts:
            existing = session.exec(select(Prompt).where(Prompt.name == p.name)).first()
            if not existing:
                session.add(p)

        session.commit()

        # 3. CHAINS
        chains_config = [
            {
                "name": "Greenshare: Full 4EM Chain",
                "prompts": [
                    "Greenshare: Sustainability Link",
                    "Greenshare: Technical Inventory",
                    "Greenshare: Rental Governance",
                    "Greenshare: Fulfillment Workflow",
                ],
            },
            {
                "name": "UrbanMicroGrid: End-to-End Logic",
                "prompts": [
                    "UrbanMicroGrid: Revenue & ESG Strategy",
                    "UrbanMicroGrid: Smart Grid Specs",
                    "UrbanMicroGrid: Trading Governance",
                    "UrbanMicroGrid: Fulfillment Workflow",
                ],
            },
        ]

        for c_cfg in chains_config:
            existing = session.exec(
                select(Chain).where(Chain.name == c_cfg["name"])
            ).first()
            if not existing:
                chain = Chain(name=c_cfg["name"], description="Full walkthrough logic.")
                session.add(chain)
                session.commit()
                session.refresh(chain)

                for i, p_name in enumerate(c_cfg["prompts"]):
                    p = session.exec(
                        select(Prompt).where(Prompt.name == p_name)
                    ).first()
                    if p:
                        session.add(
                            ChainStep(chain_id=chain.id, prompt_id=p.id, order=i + 1)
                        )
                session.commit()

        # 4. INITIAL HISTORY & AUDIT (for "lived-in" feel)
        history_check = session.exec(select(ExecutionHistory)).first()
        if not history_check:
            p = session.exec(
                select(Prompt).where(Prompt.name == "Greenshare: Sustainability Link")
            ).first()
            if p:
                h = ExecutionHistory(
                    prompt_id=p.id,
                    inputs='{"equipment": "Tesla Harvester"}',
                    result="Initial strategic approval for Tesla Harvester sharing.",
                )
                session.add(h)

                a = AuditLog(
                    user_id=architect.id,
                    action="Executed Model",
                    target_type="prompt",
                    target_id=p.id,
                    details="Baseline sustainability scan completed.",
                )
                session.add(a)

        session.commit()
        print("🚀 Codebase Environment Seeded Successfully.")


if __name__ == "__main__":
    seed()
