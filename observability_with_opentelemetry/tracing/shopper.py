import requests
from opentelemetry import trace
from opentelemetry.trace import Tracer, Status, StatusCode
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
from common import config_batch_tracer
from opentelemetry.propagate import inject
from fastapi import status


def call_request(tracer: Tracer, service_name, url):
    with tracer.start_as_current_span(
            f"call request from {service_name}",
            kind=trace.SpanKind.CLIENT,
            set_status_on_exception=True,
    ) as span:
        headers = {}
        inject(headers)
        span.add_event("request send")
        resp = requests.get(url, headers=headers)
        span.add_event("request sent", attributes={"url": url})
        span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, resp.status_code)
        if resp.status_code == status.HTTP_200_OK:
            span.set_status(Status(StatusCode.OK))
        else:
            span.set_status(Status(StatusCode.ERROR, "status code: {}".format(resp.status_code)))
            # The description field will only be used if the status code is set to ERROR;
            # it is ignored otherwise.


def get_from_grocery_store(tracer: Tracer):
    with tracer.start_as_current_span(
            "call grocery",
            kind=trace.SpanKind.CLIENT,
            record_exception=True
    ) as span:
        try:
            url = "http://localhost:5000/grocery"
            span.set_attributes({
                SpanAttributes.HTTP_METHOD: "GET",
                SpanAttributes.HTTP_FLAVOR:
                    str(HttpFlavorValues.HTTP_1_1),
                SpanAttributes.HTTP_URL: url,
                SpanAttributes.NET_PEER_IP: "127.0.0.1",
            })

            call_request(tracer, "grocery", url)
        except Exception as err:
            span.record_exception(err)


def add_item_to_cart(tracer: Tracer, *, item: str, count: int):
    with tracer.start_as_current_span("add_item_to_cart") as span:
        span.set_attributes(
            {
                "item": item,
                "quantity": count
            }
        )
        print(f"add {item} {count} to cart")
        get_from_grocery_store(tracer)


def browse(tracer: Tracer):
    with tracer.start_as_current_span("browse"):
        add_item_to_cart(tracer, item="apple", count=4)


def call_api(tracer: Tracer):
    with tracer.start_as_current_span("call_api") as span:
        browse(tracer)
        span.set_attributes({
            SpanAttributes.HTTP_METHOD: "GET",
            SpanAttributes.HTTP_FLAVOR: HttpFlavorValues.HTTP_1_1.value,
            SpanAttributes.HTTP_URL: "http://localhost:5000",
            SpanAttributes.NET_PEER_IP: "127.0.0.1",
        })


if __name__ == "__main__":
    tracer = config_batch_tracer("shopper", "0.1.2")

    with tracer.start_as_current_span("start"):
        call_api(tracer)
