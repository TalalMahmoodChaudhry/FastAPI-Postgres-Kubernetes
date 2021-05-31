import uvicorn

from src.app.app import Api
from src.app.routes import middleware, user_authenticate_route, authors_route, books_route
from src.app.database import Base, engine

Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    uvicorn.run(Api(), host='0.0.0.0', port=8000, log_config=None)
