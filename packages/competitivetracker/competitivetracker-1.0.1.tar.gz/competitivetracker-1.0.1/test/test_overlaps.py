import responses
from competitivetracker import CompetitiveTracker


@responses.activate
def test_get_domain_overlaps():
    ct = CompetitiveTracker("fake-key")
    domain = "test_domain"
    endpoint = "/%s" % domain
    url = ct.overlaps.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.overlaps.get_domain_overlaps(domain=domain)
    assert json_output == 'yay'


@responses.activate
def test_get_narrowed_overlap():
    ct = CompetitiveTracker("fake-key")
    domain = "test_domain"
    overlap = ["test-overlap-domain"]
    endpoint = "/narrow/%s" % domain
    url = ct.overlaps.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.overlaps.get_narrowed_overlap(domain=domain, overlapDomain=overlap)
    assert json_output == 'yay'


@responses.activate
def test_get_top_competing():
    ct = CompetitiveTracker("fake-key")
    domain = "test_domain"
    endpoint = "/%s/top_competing" % domain
    url = ct.overlaps.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.overlaps.get_top_competing(domain=domain)
    assert json_output == 'yay'



