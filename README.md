# Movie_Expert_Bot

This project is a Retrieval-Augmented Generation (RAG) chatbot that answers questions about Star Wars movies. It works by reading the scripts of the original Star Wars trilogy (A New Hope, The Empire Strikes Back, and Return of the Jedi) and using them as a knowledge base. When you ask a question, the bot searches the scripts for relevant information and uses it to give you an accurate answer.

It uses OpenAI's language models to understand and answer your questions, and Qdrant as a local database to store and quickly search through the movie script text.

## How to Set Up and Run Locally

To get this project running on your local machine, follow these simple steps:

### Prerequisites
You will need Python installed on your computer (version 3.12 or higher). This project uses `uv` to manage its dependencies, which is a fast Python package installer. 

You also need an OpenAI API key to use their language models.

### Setup Instructions

1. **Get the code**: Download or clone this project repository to your computer.

2. **Navigate to the project folder**: Open your terminal or command prompt and go to the project folder.

3. **Install dependencies**: If you have `uv` installed, simply run this command to install all the required libraries:
   ```bash
   uv sync
   ```
   (If you are using standard Python tools, you can create a virtual environment and install the dependencies listed in `pyproject.toml`.)

4. **Set your API Key**: You need to provide your OpenAI API key as an environment variable so the bot can use it. 
   On Mac/Linux:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   On Windows Command Prompt:
   ```cmd
   set OPENAI_API_KEY="your-api-key-here"
   ```

5. **Run the bot**: Start the application using `uv`:
   ```bash
   uv run main.py
   ```

The script will automatically download the Star Wars scripts, save them to your local database folder, and then start an interactive chat session in your terminal where you can start asking questions.
