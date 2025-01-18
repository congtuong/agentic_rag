# AI Agent Research - Backend

This is my simple RAG AI agent research project. The project is a simple web server that can handle the request from the client and response with the result of the RAG AI agent.

## Quick start

Prerequisite:

- [Python](https://www.python.org/downloads/) (>= 3.9)

**Note**: I only test the project with Python 3.9, I'm not sure if it works with higher version of Python but it should work.
**Attention**: Before starting the backend, you need to start the Elasticsearch, Database, and Vector Database first.

First, you need to fill the `.env` file with the correct information. You can copy the `.env.example` file and fill the information.

```bash
cp .env.example .env
```

Then you need to install the required packages by running the following command.

```bash
pip install -r requirements.txt
```

Finally, you can start the server by running the following command.

```bash
python app/main.py
```

Don't forget to start the other parts of the project by following the instruction in the README.md file of each part. Backend should be started after the Elasticsearch, Database, and Vector Database.

---

Or just run the following command, Docker Compose will handle the rest for you.

```bash
docker compose up
```
