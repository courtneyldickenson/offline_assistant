# Offline Assistant (RAG-Ready Backend)

A privacy-first, local-first, plug-and-play backend for building your own AI-powered assistant.  
No cloud required; no data leaves your machine. Bring your own frontend or use the API as-is.

---

## Features

- Retrieval-Augmented Generation (RAG) Q&A over your own notes, tasks, logs, and files
- Supports local LLMs (Ollama, etc.)
- Portable, human-readable data (JSON)
- Easy to extend with scripts, plugins, or wrappers for new tasks
- Utilities for file scanning and embedding (see `/scripts`)

---

## Quickstart

1. Clone this repository and set up your Python environment:
    ```bash
    git clone https://github.com/YOURUSERNAME/offline_assistant.git
    cd offline_assistant
    /opt/homebrew/bin/python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Start your local LLM server (e.g., Ollama):
    ```bash
    ollama pull llama3
    ollama run llama3
    ```

3. Run the FastAPI backend:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at http://localhost:8000

4. Try the sample query endpoint:
    ```
    GET http://localhost:8000/query?q=What should I do today?
    ```

5. (Optional) Embed your files:
    - Place test files in `/testdata` or edit `SCAN_FOLDERS` in `scripts/embed_files.py`
    - Run:
        ```bash
        python scripts/embed_files.py
        ```
    - This will save `data/file_embeddings.json` with metadata and embeddings

---

## Data Structure

- Notes, tasks, logs:  
  Stored in `/data/sample_data.json`
- Embedded files:  
  Saved to `/data/file_embeddings.json` by the embedding script

See `/data/sample_data.json` for an example.

---

## Bring Your Own Frontend

The backend provides REST endpoints for easy integration.  
Build any UI you want—React, Streamlit, mobile, CLI, etc.—and connect to the API.  
CORS is enabled for local development.

---

## Extending

- Add scripts or utilities to `/scripts`
- Add custom skills or wrappers to `/app/tasks.py`
- Document your extensions for others

---

## Contributing

Feedback, suggestions, and improvements are welcome.  
If you have ideas for new features, notice something that can be improved, or want to share your expertise, please open an issue or submit a pull request.

---

## License

MIT
