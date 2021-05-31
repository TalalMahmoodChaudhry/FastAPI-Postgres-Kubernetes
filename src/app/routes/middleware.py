import logging
import os

from opencensus.trace.span import SpanKind
from opencensus.trace.attributes_helper import COMMON_ATTRIBUTES

from fastapi import Request

from src.app.app import Api
from src.libs.logging_handlers import initialize_logging, get_tracer

HTTP_URL = COMMON_ATTRIBUTES['HTTP_URL']
HTTP_STATUS_CODE = COMMON_ATTRIBUTES['HTTP_STATUS_CODE']

initialize_logging()
logger = logging.getLogger(os.path.basename(__file__))

api = Api()


@api.middleware("http")
async def middleware_opencensus(request: Request, call_next):
    tracer = get_tracer()
    if tracer:
        with tracer.span("main") as span:
            span.span_kind = SpanKind.SERVER

            response = await call_next(request)

            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_STATUS_CODE,
                attribute_value=response.status_code)
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_URL,
                attribute_value=str(request.url))

        return response
    else:
        return await call_next(request)