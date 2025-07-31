import uvicorn
from fastapi import FastAPI

from api.publishers import router as publishers_router
from api.authors import router as authors_router
from api.books import router as books_router
from api.users import router as users_router

app = FastAPI()

app.include_router(publishers_router)
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8964)