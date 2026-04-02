# Star Wars RAG Bot

This project is a Retrieval-Augmented Generation (RAG) chatbot that answers questions about Star Wars movies. It works by reading the scripts of the original Star Wars trilogy (*A New Hope*, *The Empire Strikes Back*, and *Return of the Jedi*) and using them as a knowledge base. 

It uses **OpenAI** language models to understand your questions, **Qdrant** as a local database to store and quickly search through the script text, **FastAPI** to serve the backend, and a modern **React (Vite)** interface for a premium chat experience.

---

## 🚀 How to Set Up and Run Locally

To get this project running on your local machine, follow these steps:

### Prerequisites
1. **Python 3.12+**. This project uses `uv` to manage its Python dependencies quickly. 
2. **Node.js** (v18+) to run the React frontend.
3. **OpenAI API Key**.

### Setup Instructions

1. **Get the code**: Clone this project repository to your computer.

2. **Navigate to the project folder**: Open your terminal.
   ```bash
   cd RAG_BOT
   ```

3. **Install Python dependencies**: 
   ```bash
   uv sync
   ```

4. **Set your API Key**: Provide your OpenAI API key as an environment variable so the bot can use it. 
   On Mac/Linux:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   On Windows Command Prompt:
   ```cmd
   set OPENAI_API_KEY="your-api-key-here"
   ```

5. **Initialize the Database**: First, you need to ingest the scripts into the local Qdrant Vector Store. Simply run the ingestion script once:
   ```bash
   uv run main.py
   ```
   Wait until it says "Star Wars RAG Bot is ready to go!", then you can type `exit` or `Ctrl+C`. Your texts are now securely embedded locally in the `./qdrant_db/` folder.

6. **Start the API Backend**: Now, boot up the FastAPI server that the frontend uses.
   ```bash
   uv run uvicorn api:app --reload
   ```

7. **Start the React Frontend**: Open a **second terminal window**, navigate to the frontend folder, and start the Vite dev server:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

Open `http://localhost:5173` in your browser. You can now chat directly with the Star Wars model through the premium Star Wars-themed frontend!
