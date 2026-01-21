# Prompt Management Tool

A tool for managing prompts and prompt chains, executing them against LLMs, and evaluating results.

## Tech Stack
- Frontend: Next.js (React), Tailwind CSS
- Backend: FastAPI (Python), SQLModel (SQLite)

## Setup:

### Backend
1. Navigate to `backend/`: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. **Environment Setup**: 
   - Copy `.env.template` to `.env`
   - Add your `OPENAI_API_KEY` to the `.env` file
4. **Data Initialization**:
   - Run the seeding script to populate the local database: `python seed.py`
   - This loads all architectural frameworks (4EM, TOGAF, etc.) into your local environment.
5. Run server: `uvicorn main:app --reload`

### Frontend
1. Navigate to `frontend/`
2. `npm install`
3. Run dev server: `npm run dev`


Participants:
- Shravan Navaneeth Kumar
- Mohammad Akmal Hassan
- Nour Aouadi
