import logging
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs.export import ConsoleLogExporter, BatchLogRecordProcessor


def configure_logger(name, version):
    provider = LoggerProvider(resource=Resource.create())
    set_logger_provider(provider)
    exporter = ConsoleLogExporter()
    provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = LoggingHandler()
    logger.addHandler(handler)
    return logger


if __name__ == "__main__":
    logger = configure_logger("shopper", "0.1.2")
    logger.info("add 1 to cart")
