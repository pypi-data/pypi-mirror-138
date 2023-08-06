import responses
from competitivetracker import CompetitiveTracker


@responses.activate
def test_search():
    ct = CompetitiveTracker("fake-key")
    qd = "test-qd"
    sendingDomain = "test_domain"
    endpoint = ""
    url = ct.search.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.search.search(qd=qd, sendingDomain=sendingDomain)
    assert json_output == 'yay'

