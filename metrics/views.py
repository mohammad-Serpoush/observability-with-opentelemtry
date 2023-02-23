from opentelemetry.metrics import Counter
from opentelemetry.sdk.metrics._internal.aggregation import DropAggregation
from opentelemetry.sdk.metrics._internal.view import View

views_1 = [
    View(
        instrument_name="",
        aggregation=DropAggregation()
    ),
    View(
        instrument_type=Counter,
        attribute_keys=set(),
        name="sold",
        description="total item sold",
    ),
]

views_2 = [
    View(
        instrument_name="",
        aggregation=DropAggregation()
    ),
    View(
        instrument_type=Counter,
        attribute_keys={"locale"},
    ),
]
