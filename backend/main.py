from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.auth import auth_router
from backend.routers.users import user_router
from backend.routers.chats import chat_router
from backend.database import create_db_and_tables,EntityNotFoundException, DuplicateEntityException
from backend.auth import DuplicateEntityException_Auth
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan = lifespan,
    title="buddy system API",
    description="API for managing fosters and adoptions.",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(chat_router)

@app.exception_handler(DuplicateEntityException_Auth)
def handle_duplicate_entity_auth( _request: Request,
    exception: DuplicateEntityException_Auth,
) -> JSONResponse:
    # logging.exception(f"Duplicate Entity Exception: {exception}")

    return JSONResponse(
        status_code = 422,
        content={
            "detail": {
                "type": "duplicate_value",
                "entity_name": 'User',
                "entity_field": exception.entity_field,
                "entity_value": exception.entity_value,
            },
        },
    )

@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
    _request: Request,
    exception: EntityNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": {
                "type": "entity_not_found",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )

@app.exception_handler(DuplicateEntityException)
def handle_duplicate_entity(
    _request: Request,
    exception: DuplicateEntityException,
) -> JSONResponse:
    # logging.exception(f"Duplicate Entity Exception: {exception}")

    return JSONResponse(
        status_code = 422,
        content={
            "detail": {
                "type": "duplicate_entity",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )