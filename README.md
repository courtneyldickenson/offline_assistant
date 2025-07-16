# Offline Assistant (RAG-Ready Backend)

A privacy-first, local-first, plug-and-play backend for building your own AI-powered assistant.  
No cloud required; no data leaves your machine. Bring your own frontend and connect any LLM—Ollama, LM Studio, LocalAI, llama.cpp, etc.—for 100% local inference.

---

## Features

- Retrieval-Augmented Generation (RAG) Q&A over your notes, tasks, logs, and documents
- Scans and ingests local files (PDF, TXT, DOCX, CSV, etc.)
- Plug-and-play: Attaches to any LLM running locally or on your LAN (Ollama, LM Studio, LocalAI, llama.cpp, etc.)
- Portable, human-readable config (`config.yaml`)
- All embeddings stored locally with ChromaDB (never sent to cloud)
- FastAPI backend with clean REST endpoints for search and learning
- Modular, extensible code—easy to add scripts, plugins, or new skills
- Utilities for file scanning, snippet extraction, and embedding (see `/app/watch_desktop.py`, `/app/ingest_files.py`)

---

## Quickstart

**This project runs on macOS, Linux, and Windows.**

1. **Clone the repository and set up your Python environment:**
    ```sh
    git clone https://github.com/YOURUSERNAME/offline_assistant.git
    cd offline_assistant
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    # venv\Scripts\activate
    pip install -r requirements.txt
    ```

2. **Configure which folders to scan:**
    - Edit the `folders` section in `config.yaml` to list the directories you want to index.
    - Example:
      ```yaml
      folders:
        - ~/Desktop
        - ~/Documents
      ```

3. **Scan and queue your files for learning:**
    ```sh
    python app/watch_desktop.py
    ```
    This will queue all new/unprocessed files for learning.

4. **Ingest queued files (process and embed):**
    ```sh
    python app/ingest_files.py
    ```
    This processes each queued file, extracts text, and stores embeddings in ChromaDB.

5. **(Optional) Start your LLM backend:**
    - Run Ollama, LM Studio, LocalAI, etc., locally.  
    - Configure your LLM API endpoint and model in your `.env` file or as environment variables:
      ```
      LLM_API_URL=http://localhost:11434
      LLM_MODEL=llama3
      ```

6. **Run the FastAPI backend:**
    ```sh
    uvicorn app.main:app --reload
    ```
    The API will be available at http://localhost:8000

7. **Try the API endpoints:**
    - **Add document:**  
      `POST http://localhost:8000/add`
    - **Search (RAG/Q&A):**  
      `POST http://localhost:8000/search`
    - **Learn custom text:**  
      `POST http://localhost:8000/learn`
    - **Full scan and ingest:**  
      `POST http://localhost:8000/scan`
    - _(Swagger/OpenAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs))_

---

## Configuration

- **Folders to watch:** Set in `config.yaml` under `folders:`
- **File types to skip:** Set in `config.yaml` under `skip_exts:`
- **ChromaDB path:** Set in `config.yaml` or via the `CHROMA_DB_PATH` environment variable
- **LLM Backend:** Set `LLM_API_URL` and `LLM_MODEL` in `.env` or your environment

---

## Data Structure

- All embeddings and file metadata are stored locally in ChromaDB (`chroma_data/` by default)
- No personal or sensitive data leaves your machine
- Example config and sample data are provided in the repo

---

## Bring Your Own Frontend

The backend exposes clean REST endpoints for integration with any UI—React, Streamlit, CLI, or mobile.  
CORS is enabled for local development.

---

## Extending

- Add scripts or utilities to `/scripts`
- Add custom skills or wrappers to `/app/tasks.py`
- Document your extensions for others

---

## Contributing

Feedback, suggestions, and improvements are welcome!  
If you have ideas for new features, spot something to improve, or want to share your expertise, please open an issue or submit a pull request.

---

## Notes

- **Virtual Environment Activation:**  
    - macOS/Linux: `source venv/bin/activate`
    - Windows: `venv\Scripts\activate`
- **Python version:**  
    - Python 3.8+ recommended
- **Troubleshooting:**  
    - If you hit permissions errors, check file/folder permissions for ChromaDB (`chroma_data/`)
    - If you see DB errors, make sure the directory is writable by your user
    - See Issues section for platform-specific tips

---

## License

MIT

