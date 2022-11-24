from apibara.indexer.events import EventFilter, EventMatcher
from tests.conftest import load_json_fixture


def test_event_matcher():
    data = load_json_fixture("block_11000.json")
    block = data["data"]["data"]

    filters = [
        EventFilter.from_event_name(
            "Transfer",
            address="0x07861c4e276294a7e859ff0ae2eec0c68300ad9cbb43219db907da9bad786488",
        ),
    ]

    matcher = EventMatcher(filters)
    events = matcher.find_events_in_block(block)
    assert len(events) == 8

    filters = [EventFilter.from_event_name("deposit_handled")]
    matcher.replace_filters(filters)
    events = matcher.find_events_in_block(block)
    assert len(events) == 9

    filters = [
        EventFilter.from_event_name(
            "Transfer",
            address="0x07861c4e276294a7e859ff0ae2eec0c68300ad9cbb43219db907da9bad786488",
        ),
        EventFilter.from_event_name("deposit_handled"),
    ]
    matcher.replace_filters(filters)
    events = matcher.find_events_in_block(block)
    assert len(events) == 17

    filters = [
        EventFilter.from_event_name(
            "deposit_handled",
            address="0x07861c4e276294a7e859ff0ae2eec0c68300ad9cbb43219db907da9bad786488",
        ),
    ]
    matcher.replace_filters(filters)
    events = matcher.find_events_in_block(block)
    assert events == []
