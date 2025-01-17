# AI Agent Research - Frontend

This is my simple RAG AI agent research project. The project is a simple web server that can handle the request from the client and response with the result of the RAG AI agent.

## Quick start

Prerequisite:

<!-- - [Python](https://www.python.org/downloads/) (>= 3.9) -->

- [Node](https://nodejs.org/en/download/) (>= 22)
- [Bun](https://bun.sh/)

In this project, I use Bun to manage the project. You are free to use any package manager you want.

```bash
npm install -g bun
```

#### Start the project

First, you need to fill the `.env` file with the correct information. You can copy the `.env.example` file and fill the information.

```bash
cp .env.example .env
```

Then you need to install the required packages by running the following command.

```bash
bun install
```

Finally, you can start the server by running the following command.

```bash
bun run build && bun run start
```

Don't forget to start the other parts of the project by following the instruction in the README.md file of each part.

---

Or just run the following command, Docker Compose will handle the rest for you.

```bash
docker compose up
```
