Enterprise Modelling Tool Frontend

This is the frontend application for the Enterprise Modelling Tool, built with [Next.js](https://nextjs.org) and Tailwind CSS. It provides a visual workbench for architects to manage prompts, execute chains, and view enterprise models.

Technology Stack

- Framework: Next.js 14 (App Router)
- Styling: Tailwind CSS, Shadcn UI (Lucide React icons)
- State Management: React Context (AuthContext)
- Data Fetching: Axios

Getting Started

1. Install dependencies:
    npm install
    or
    yarn install
    

2. Run the development server:
    npm run dev
    

3. Open the application:
    Open http://localhost:3000 with your browser.

Project Structure

- src/app: App Router pages and layouts.
- src/components: Reusable UI components.
- src/services: API client definitions (api.ts).
- src/context: Global state providers (Authentication).

Features

- Architect Workbench: Specialized dashboard for Enterprise Architects.
- Pattern Library: Manage and edit generative AI prompts.
- Chain Architect: Design sequential logic flows.
- Activity Log: Real-time tracking of model executions.
