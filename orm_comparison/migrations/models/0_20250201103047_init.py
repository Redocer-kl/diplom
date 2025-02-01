from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128) NOT NULL
);
CREATE TABLE IF NOT EXISTS "task" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "title" VARCHAR(200) NOT NULL,
    "description" TEXT NOT NULL,
    "is_completed" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
