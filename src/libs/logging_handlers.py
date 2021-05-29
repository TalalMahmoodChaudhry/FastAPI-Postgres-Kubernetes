import logging
import os
import sys

from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace import config_integration
from opencensus.trace.tracer import Tracer
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler

config_integration.trace_integrations(['logging', 'postgresql'])
INSTRUMENTATION_KEY = os.environ.get("APPLICATION_INSIGHTS_KEY")

LOG_FORMAT = '%(levelname) -0s %(asctime)s %(name) -20s %(funcName) -35s %(lineno) -5d: %(message){}s'.format('')

config_integration.trace_integrations(['logging', 'postgresql', 'requests'])


def initialize_logging() -> None:
    stream_handler = logging.StreamHandler(sys.stdout)
    handlers = [stream_handler]

    try:
        azure_handler = AzureLogHandler(connection_string=INSTRUMENTATION_KEY)
        handlers.append(azure_handler)
    except ValueError:
        pass

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=handlers)


def get_tracer():
    try:
        return Tracer(exporter=AzureExporter(connection_string=INSTRUMENTATION_KEY),
                      sampler=ProbabilitySampler(1.0))
    except ValueError:
        return None
