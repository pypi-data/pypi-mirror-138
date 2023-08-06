import responses
from competitivetracker import CompetitiveTracker


@responses.activate
def test_ping_service():
    CT = CompetitiveTracker("fake-key")
    endpoint = ""
    url = CT.ping.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "pong"}'
    )
    output = CT.ping.ping_service()
    assert output == "pong"
