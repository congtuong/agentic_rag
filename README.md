# AI Agent Research

This is my simple RAG AI agent research project. The project is a simple web server that can handle the request from the client and response with the result of the RAG AI agent.

## Project Flow

The basic flow of the application is as follows:

1. **User Login**: Users authenticate and log in to the system.
2. **Upload Documents**: Users can upload documents that they want the AI agent to learn from.
3. **Create a Custom Chatbot**: Based on the uploaded documents, multiple personalized RAG-based chatbot is created for each user.
4. **Interact with the Chatbot**: Users can then chat with their custom chatbot, which leverages retrieval-augmented generation for accurate and context-aware responses.

> This architecture lays the foundation for developing a **SaaS platform** that provides **customized chatbots** for companies or individuals. Each user or organization can have its own isolated chatbot environment powered by the documents they upload.

## System overview

This project contains 5 main parts:

- **Backend**: The Python server that handle the request from the client and response with the result of the RAG AI agent.
- **Frontend**: The NextJS web client that send the request to the server and display the result.
- **Elasitcsearch**: The Elasticsearch server that store the chunks of the documents, minimize the pressure on the database.
- **Database**: The SQLite or Postgres relational database.
- **Vector Database**: The vector database that store the vector of the documents. Currently, I use the Milvus server.

## Quick start

To start the project, you can just start each part of the project by following the instruction in the README.md file of each part.

Or just run the following command, Docker Compose will handle the rest for you.

```bash
docker compose up
```

## Development

I'm still working on this project, so there are still many things to do. If you want to contribute to this project, feel free to fork this project and create a pull request. I will review your code and merge it if it's good.

List of things that I want to do:

- [ ] Use the Elasticsearch vector search and kNN search to improve the performance of the search.
- [ ] Try to use the other alternative of RAG like CAG.
- [ ] Support more database like MySQL, MariaDB, etc.
- [ ] Support more vector database like Faiss, Annoy, etc.
- [ ] Add more documentation
- [ ] Add more test
