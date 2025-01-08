-- Enums need to be emulated in SQLite, using a CHECK constraint
CREATE TABLE "role" (
  "value" TEXT PRIMARY KEY CHECK ("value" IN ('admin', 'user'))
);

CREATE TABLE "chatbot_status" (
  "value" TEXT PRIMARY KEY CHECK ("value" IN ('private', 'public'))
);

CREATE TABLE "sender_type" (
  "value" TEXT PRIMARY KEY CHECK ("value" IN ('assistant', 'user'))
);

CREATE TABLE "users" (
  "id" TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  "username" TEXT UNIQUE NOT NULL,
  "email" TEXT UNIQUE NOT NULL,
  "password" TEXT NOT NULL,
  "user_fullname" TEXT NOT NULL,
  "user_role" TEXT NOT NULL DEFAULT 'user' CHECK ("user_role" IN ('admin', 'user')),
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE "sessions" (
  "id" TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  "user_id" TEXT NOT NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY ("user_id") REFERENCES "users" ("id")
);

CREATE TABLE "documents" (
  "id" TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  "user_id" TEXT NOT NULL,
  "object_name" TEXT NOT NULL,
  "file_name" TEXT NOT NULL,
  "file_type" TEXT NOT NULL,
  "file_size" REAL NOT NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY ("user_id") REFERENCES "users" ("id")
);

CREATE TABLE "chunks" (
  "id" TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  "document_id" TEXT NOT NULL,
  "chunk_index" INTEGER NOT NULL,
  "vector_id" TEXT NOT NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY ("document_id") REFERENCES "documents" ("id")
);

CREATE TABLE "knowledges" (
  "id" TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  "user_id" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY ("user_id") REFERENCES "users" ("id")
);

CREATE TABLE "knowledge_documents" (
  "knowledge_id" TEXT NOT NULL,
  "document_id" TEXT NOT NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY ("knowledge_id", "document_id"),
  FOREIGN KEY ("knowledge_id") REFERENCES "knowledges" ("id"),
  FOREIGN KEY ("document_id") REFERENCES "documents" ("id")
);

CREATE TABLE "chatbot_knowledges" (
  "chatbot_id" TEXT NOT NULL,
  "knowledge_id" TEXT NOT NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY ("chatbot_id", "knowledge_id"),
  FOREIGN KEY ("chatbot_id") REFERENCES "chatbots" ("id"),
  FOREIGN KEY ("knowledge_id") REFERENCES "knowledges" ("id")
);

CREATE TABLE "chatbots" (
  "id" TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  "user_id" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "config" TEXT NOT NULL, -- JSON is stored as TEXT in SQLite
  "status" TEXT NOT NULL CHECK ("status" IN ('private', 'public')),
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE "conversations" (
  "id" TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  "chatbot_id" TEXT NOT NULL,
  "user_id" TEXT NOT NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY ("chatbot_id") REFERENCES "chatbots" ("id"),
  FOREIGN KEY ("user_id") REFERENCES "users" ("id")
);

CREATE TABLE "messages" (
  "id" TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  "conversation_id" TEXT NOT NULL,
  "content" TEXT NOT NULL,
  "type" TEXT NOT NULL CHECK ("type" IN ('assistant', 'user')),
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY ("conversation_id") REFERENCES "conversations" ("id")
);

-- Insert initial data
INSERT INTO "users" ("username", "email", "password", "user_fullname", "user_role") VALUES (
  'admin', 'tuongbck@gmail.com', 
  '$2a$10$VFKP3WQvhZRb7CGVag1li.6DjtTKqp3tIoTpDLGPIY4pGQvwC1QXm', 'Cong Tuong', 'admin'
);
