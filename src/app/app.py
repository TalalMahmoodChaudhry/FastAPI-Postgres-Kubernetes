from fastapi import FastAPI

from src.libs.wrappers import singleton


@singleton
class Api(FastAPI):
    @property
    def app(self):
        return Api()
