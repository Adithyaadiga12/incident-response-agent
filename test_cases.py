TEST_CASES = [
    # crash fault, different alert phrasings
    {"id": "crash-1", "fault": "crash", "alert": "Users report errors on /data.", "expect": ["database", "connection"]},
    {"id": "crash-2", "fault": "crash", "alert": "500 errors spiking on the service.", "expect": ["database", "connection"]},
    {"id": "crash-3", "fault": "crash", "alert": "The /data endpoint is down.", "expect": ["database", "connection"]},

    # errors fault
    {"id": "errors-1", "fault": "errors", "alert": "Intermittent failures on /data.", "expect": ["upstream"]},
    {"id": "errors-2", "fault": "errors", "alert": "Some requests to /data are failing.", "expect": ["upstream"]},
    {"id": "errors-3", "fault": "errors", "alert": "Flaky errors reported by users.", "expect": ["upstream"]},

    # slow fault
    {"id": "slow-1", "fault": "slow", "alert": "The /data endpoint is slow.", "expect": ["slow", "latency", "delay"]},
    {"id": "slow-2", "fault": "slow", "alert": "High response times on the service.", "expect": ["slow", "latency", "delay"]},
    {"id": "slow-3", "fault": "slow", "alert": "Users complain about timeouts.", "expect": ["slow", "latency", "delay"]},

    # healthy — agent must NOT invent a problem
    {"id": "none-1", "fault": "none", "alert": "Routine health check on /data.", "expect": ["no", "healthy", "normal", "no issue", "no problem"]},
]