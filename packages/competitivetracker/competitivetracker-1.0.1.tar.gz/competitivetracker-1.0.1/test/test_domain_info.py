import responses
from competitivetracker import CompetitiveTracker


@responses.activate
def test_get_brand_volume_and_esps():
    ct = CompetitiveTracker("fake-key")
    domain = "test_domain"
    endpoint = "/brand_volume_average_and_esps"
    url = ct.domain_info.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    responses.add(
        responses.POST,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.domain_info.get_brand_volume_and_esps(domains=domain)
    assert json_output == 'yay'


@responses.activate
def test_get_domain_info():
    ct = CompetitiveTracker("fake-key")
    domain = "test_domain"
    endpoint = ""
    url = ct.domain_info.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.domain_info.get_domain_info(domain=domain)
    assert json_output == 'yay'
