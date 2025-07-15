# Offline Assistant (RAG-Ready Backend)

A privacy-first, local-first, plug-and-play backend for building your own AI-powered assistant.  
No cloud required; no data leaves your machine. Bring your own frontend and connect any LLM—Ollama, LM Studio, LocalAI, llama.cpp, etc.—to handle inference.

---

## Features

- Retrieval-Augmented Generation (RAG) Q&A over your own notes, tasks, logs, and files
- Scans and ingests local files (documents, notes, etc.)
- Attaches to any LLM running locally or on your LAN (Ollama, LM Studio, LocalAI, llama.cpp, etc.)
- Portable, human-readable data (JSON)
- Easy to extend with scripts, plugins, or wrappers for new tasks
- Utilities for file scanning and embedding (see `/app/watch_desktop.py`, `/app/ingest_files.py`, and `/scripts`)

---

## Quickstart

**This project runs on macOS, Linux, and Windows. The commands below are universal—see notes if you run into platform-specific issues.**

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

2. **Scan and queue your files for learning:**
    - Edit `FOLDERS` in `app/watch_desktop.py` to point to folders you want to scan.
    - Run:
        ```sh
        python app/watch_desktop.py
        ```
    - This will queue new/unseen files for learning.

3. **Ingest queued files (process and embed):**
    ```sh
    python app/ingest_files.py
    ```
    - This will process each queued file, extract text, and create/update embeddings in `/data/file_embeddings.json`.

4. **Attach your LLM backend:**
    - Start your preferred LLM server (e.g., Ollama, LM Studio, LocalAI, llama.cpp, etc.)
    - Update the model/backend URL in your environment config or `.env` file if required (see below).
    - The API will use this backend for inference.

5. **Run the FastAPI backend:**
    ```sh
    uvicorn app.main:app --reload
    ```
    The API will be available at http://localhost:8000

6. **Try the API endpoints:**
    - **Add document:**  
      `POST http://localhost:8000/add`
    - **Search (RAG/Q&A):**  
      `POST http://localhost:8000/search`
    - **Learn custom text:**  
      `POST http://localhost:8000/learn`
    - _(OpenAPI docs available at [http://localhost:8000/docs](http://localhost:8000/docs) with schemas and example requests)_

---

## Configuration

- **To use a specific LLM backend:**  
  Set the LLM API URL (and model name, if needed) in your `.env` file or as environment variables.  
  Example for Ollama:
    ```
    LLM_API_URL=http://localhost:11434
    LLM_MODEL=llama3
    ```
  For other backends, use their API docs to get the correct URL/model name.

---

## Data Structure

- Notes, tasks, logs:  
  Stored in `/data/sample_data.json`
- Embedded files:  
  Saved to `/data/file_embeddings.json` by the ingestion scripts

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

## Notes

- **Virtual Environment Activation:**  
    - On macOS/Linux: `source venv/bin/activate`
    - On Windows: `venv\Scripts\activate`
- **Python:**  
    - If `python` doesn’t work, try `python3` or `py` depending on your OS.
- **If you run into issues:**  
    - Make sure you have Python 3.8+ and pip installed.
    - Check [the official Python documentation](https://docs.python.org/3/library/venv.html) for help with virtual environments.
    - For platform-specific problems, see the Issues section or open a new issue.

---

## License

MIT
