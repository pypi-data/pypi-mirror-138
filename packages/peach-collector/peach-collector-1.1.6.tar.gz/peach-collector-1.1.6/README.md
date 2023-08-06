# peach-collector

Peach Collector client implementation in Python 3.8


# PeachCollector

Simplest way to send events.

    collector = PeachCollector("a-site-key", "an-app-id")
    collector.add_event({"type":"an-event-type", foo": 666})
    collector.add_event({"type":"an-event-type", "bar": 777})
    await collector.send_events()


# PeachCollectorQueue

Pushes events on to a Redis queue which is drained at regular intervals.

    # Client
    q = PeachCollectorQueue("redis://localhost")
    q.push_event({"type":"an-event-type", "foo": 66})
    q.push_event({"type":"an-event-type", "bar": 777})

    # Scheduled Worker
    collector = PeachCollector("a-site-key", "an-app-id")
    q = PeachCollectorQueue("redis://localhost", collector)
    q.drain()
