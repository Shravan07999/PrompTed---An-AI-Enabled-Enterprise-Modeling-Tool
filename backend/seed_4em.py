from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import Prompt, Chain, ChainStep

def seed_4em_data():
    create_db_and_tables()
    
    with Session(engine) as session:
        # Check if data already exists to avoid duplicates
        existing = session.exec(select(Prompt).where(Prompt.name == "4EM: Goal Model")).first()
        if existing:
            print("4EM data already exists. Skipping.")
            return

        # 1. Goal Model
        p_goals = Prompt(
            name="4EM: Goal Model",
            description="Identify strategic goals and objectives.",
            template="You are an enterprise architect using the 4EM method. Identify the strategic goals, critical success factors, and problems for {{organization}} regarding {{topic}}.\n\nOutput format:\n- Goals:\n- Problems:\n- Success Factors:",
            input_variables="organization, topic",
            tags="4EM, Goals"
        )
        session.add(p_goals)

        # 2. Business Process Model
        p_process = Prompt(
            name="4EM: Business Process Model",
            description="Outline business processes and workflows.",
            template="Based on the goal '{{goal}}', outline the high-level business process. Identify the main activities, information flows, and decision points.",
            input_variables="goal",
            tags="4EM, Process"
        )
        session.add(p_process)

        # 3. Concepts Model
        p_concepts = Prompt(
            name="4EM: Concepts Model",
            description="Define key concepts and terminology.",
            template="Define the key concepts, entities, and attributes relevant to {{domain}}. Ensure clear definitions to avoid ambiguity.",
            input_variables="domain",
            tags="4EM, Concepts"
        )
        session.add(p_concepts)

        # 4. Business Rules Model
        p_rules = Prompt(
            name="4EM: Business Rules Model",
            description="Define business rules and constraints.",
            template="List the operational business rules and constraints that govern the process of {{process}}. Format as 'IF <condition> THEN <action>'.",
            input_variables="process",
            tags="4EM, Rules"
        )
        session.add(p_rules)

        # 5. Actors & Resources Model
        p_actors = Prompt(
            name="4EM: Actors & Resources",
            description="Identify actors and resources.",
            template="Identify the human actors, organizational units, and physical/informational resources required for {{activity}}.",
            input_variables="activity",
            tags="4EM, Actors"
        )
        session.add(p_actors)

        # 6. Technical Components Model
        p_tech = Prompt(
            name="4EM: Technical Components",
            description="Identify technical systems and infrastructure.",
            template="List the software applications, hardware, and technical infrastructure needed to support {{process}}.",
            input_variables="process",
            tags="4EM, Technical"
        )
        session.add(p_tech)
        
        session.commit()
        
        # Refresh to get IDs
        session.refresh(p_goals)
        session.refresh(p_process)

        # Create a Chain: Goal -> Process
        chain = Chain(
            name="4EM: Strategic Process Alignment",
            description="Derive business processes from strategic goals."
        )
        session.add(chain)
        session.commit()
        session.refresh(chain)

        # Step 1: Goals
        step1 = ChainStep(
            chain_id=chain.id,
            prompt_id=p_goals.id,
            order=1
        )
        session.add(step1)

        # Step 2: Process
        # In a real scenario, we'd map the output of step 1 to 'goal' input of step 2.
        # For now, we just add the step.
        step2 = ChainStep(
            chain_id=chain.id,
            prompt_id=p_process.id,
            order=2,
            input_mapping='{"goal": "output_from_step_1"}' # Conceptual mapping
        )
        session.add(step2)
        
        session.commit()
        print("Successfully seeded 4EM prompts and chain.")

if __name__ == "__main__":
    seed_4em_data()
