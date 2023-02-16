from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from resource_detector import LocalResourceDetector


def config_batch_tracer(name, version):
    exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(exporter)
    local_resource = LocalResourceDetector().detect()
    resource = local_resource.merge(
        Resource.create(
            {
                "service.name": name,
                "service.version": version,
            }
        )
    )
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(span_processor=span_processor)
    trace.set_tracer_provider(tracer_provider=provider)
    return trace.get_tracer(name, version)

# def configure_tracer():
#     exporter = ConsoleSpanExporter()
#     span_processor = SimpleSpanProcessor(exporter)
#     provider = TracerProvider()
#     provider.add_span_processor(span_processor)
#     trace.set_tracer_provider(provider)
#     return trace.get_tracer("shopper.py", "0.0.1")
