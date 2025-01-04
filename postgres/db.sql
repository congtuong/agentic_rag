CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE "role" AS ENUM (
  'admin',
  'user'
);

CREATE TYPE "chatbot_status" AS ENUM (
  'private',
  'public'
);

CREATE TYPE "sender_type" AS ENUM (
  'assistant',
  'user'
);

CREATE TABLE "users" (
  "id" UUID PRIMARY KEY DEFAULT (uuid_generate_v4()),
  "username" varchar(25) UNIQUE NOT NULL,
  "email" varchar(50) UNIQUE NOT NULL,
  "password" text NOT NULL,
  "user_fullname" text NOT NULL,
  "user_role" role NOT NULL DEFAULT 'user',
  "created_at" timestamp NOT NULL DEFAULT (now()),
  "updated_at" timestamp NOT NULL DEFAULT (now())
);

CREATE TABLE "documents" (
  "id" UUID PRIMARY KEY DEFAULT (uuid_generate_v4()),
  "user_id" UUID NOT NULL,
  "object_name" text NOT NULL,
  "file_name" text NOT NULL,
  "file_type" varchar(5) NOT NULL,
  "file_size" float NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT (now()),
  "updated_at" timestamp NOT NULL DEFAULT (now())
);

CREATE TABLE "chunks" (
  "id" UUID PRIMARY KEY DEFAULT (uuid_generate_v4()),
  "document_id" UUID NOT NULL,
  "chunk_index" int NOT NULL,
  "vector_id" text NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT (now()),
  "updated_at" timestamp NOT NULL DEFAULT (now())
);

CREATE TABLE "knowledges" (
  "id" UUID PRIMARY KEY DEFAULT (uuid_generate_v4()),
  "user_id" UUID NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT (now()),
  "updated_at" timestamp NOT NULL DEFAULT (now())
);

CREATE TABLE "knowledge_documents" (
  "knowledge_id" UUID NOT NULL,
  "document_id" UUID NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT (now()),
  "updated_at" timestamp NOT NULL DEFAULT (now()),
  PRIMARY KEY ("knowledge_id", "document_id")
);

CREATE TABLE "chatbot_knowledges" (
  "chatbot_id" UUID NOT NULL,
  "knowledge_id" UUID NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT (now()),
  "updated_at" timestamp NOT NULL DEFAULT (now()),
  PRIMARY KEY ("chatbot_id", "knowledge_id")
);

CREATE TABLE "chatbots" (
  "id" UUID PRIMARY KEY DEFAULT (uuid_generate_v4()),
  "user_id" UUID NOT NULL,
  "name" varchar(50) NOT NULL,
  "config" json NOT NULL,
  "status" chatbot_status NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT (now()),
  "updated_at" timestamp NOT NULL DEFAULT (now())
);

CREATE TABLE "conversations" (
  "id" UUID PRIMARY KEY DEFAULT (uuid_generate_v4()),
  "chatbot_id" UUID NOT NULL,
  "user_id" UUID NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT (now()),
  "updated_at" timestamp NOT NULL DEFAULT (now())
);

CREATE TABLE "messages" (
  "id" UUID PRIMARY KEY DEFAULT (uuid_generate_v4()),
  "conversation_id" UUID NOT NULL,
  "content" text NOT NULL,
  "type" sender_type NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT (now()),
  "updated_at" timestamp NOT NULL DEFAULT (now())
);

ALTER TABLE "documents" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "chunks" ADD FOREIGN KEY ("id") REFERENCES "documents" ("id");

ALTER TABLE "knowledges" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "knowledge_documents" ADD FOREIGN KEY ("knowledge_id") REFERENCES "knowledges" ("id");

ALTER TABLE "knowledge_documents" ADD FOREIGN KEY ("document_id") REFERENCES "documents" ("id");

ALTER TABLE "chatbot_knowledges" ADD FOREIGN KEY ("knowledge_id") REFERENCES "knowledges" ("id");

ALTER TABLE "chatbot_knowledges" ADD FOREIGN KEY ("chatbot_id") REFERENCES "chatbots" ("id");

ALTER TABLE "conversations" ADD FOREIGN KEY ("chatbot_id") REFERENCES "chatbots" ("id");

ALTER TABLE "messages" ADD FOREIGN KEY ("conversation_id") REFERENCES "conversations" ("id");
