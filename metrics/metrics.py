from opentelemetry.metrics import set_meter_provider, get_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.metrics._internal.observation import Observation
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server
import resource


def configure_meter_provider():
    start_http_server(port=8000, addr="localhost")
    reader = PrometheusMetricReader(prefix="MetricExample")
    exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
    provider = MeterProvider(metric_readers=[reader], resource=Resource.create())
    set_meter_provider(provider)


def async_gauge_callback(callback_option):

    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return [Observation(rss, {"app": "timescale"})]


if __name__ == "__main__":
    configure_meter_provider()
    meter = get_meter_provider().get_meter(
        name="metric-example",
        version="0.1.2",
        schema_url="https://opentelemetry.io/schemas/1.9.0"
    )
    counter = meter.create_counter(
        "item_sold",
        "items",
        description="Total items sold"
    )
    counter.add(6, {"locale": "fr-FR", "country": "CA"})
    counter.add(1, {"locale": "es-ES"})

    inventory_counter = meter.create_up_down_counter(
        name="inventory",
        unit="items",
        description="Number of items in inventory"
    )
    inventory_counter.add(20)
    inventory_counter.add(-5)

    histogram = meter.create_histogram(
        "response_times",
        unit="ms",
        description="Response time fo all requests",
    )
    histogram.record(96)
    histogram.record(9)

    meter.create_observable_gauge(
        name="maxrss",
        unit="bytes",
        callbacks=[async_gauge_callback],
        description="Max resident set size"
    )
    input("Press anything to continue... ")
