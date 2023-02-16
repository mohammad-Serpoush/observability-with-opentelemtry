import uvicorn as uvicorn
from fastapi import FastAPI, Request
from opentelemetry.trace import Tracer, SpanKind
from fastapi import Depends
from opentelemetry.semconv.trace import SpanAttributes

from common import config_batch_tracer

app = FastAPI()


def get_tracer():
    tracer = config_batch_tracer("grocery", "1.2.3")
    return tracer


@app.get("/grocery")
def get_grocery(
        *,
        tracer: Tracer = Depends(get_tracer),
        request: Request
):
    with tracer.start_as_current_span("get_grocery", kind=SpanKind.SERVER) as span:
        span.set_attributes({
            SpanAttributes.HTTP_METHOD: request.method,
        })
    return "ok"


if __name__ == "__main__":
    uvicorn.run(app, port=5000)
