import responses
from competitivetracker import CompetitiveTracker


@responses.activate
def test_campaign_get_campaign():
    ct = CompetitiveTracker("fake-key")
    campaignId = "test-campaign"
    endpoint = "/campaign/%s" % campaignId
    url = ct.intelligence.campaign.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.campaign.get_campaign(campaignId=campaignId)
    assert json_output == 'yay'


@responses.activate
def test_campaign_get_target_country():
    ct = CompetitiveTracker("fake-key")
    campaignId = "test-campaign"
    endpoint = "/campaign/targetCountry/%s" % campaignId
    url = ct.intelligence.campaign.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.campaign.get_target_country(campaignId=campaignId)
    assert json_output == 'yay'


@responses.activate
def test_brand_get_top_domains():
    ct = CompetitiveTracker("fake-key")
    brandId = "test-brand"
    endpoint = "/brand/%s/top_domains" % brandId
    url = ct.intelligence.brand.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.brand.get_top_domains(brandId=brandId)
    assert json_output == 'yay'


@responses.activate
def test_ipdeliverability_get_agg_stats_for_range():
    ct = CompetitiveTracker("fake-key")
    qd = "test-qd"
    startingIpAddress = "test-ip"
    endpoint = "/ipdeliverability/range/%s/totalVolume" % startingIpAddress
    url = ct.intelligence.ipdeliverability.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.ipdeliverability.get_agg_stats_for_range(qd=qd, startingIpAddress=startingIpAddress)
    assert json_output == 'yay'


@responses.activate
def test_ipdeliverability_get_deliverability_stats():
    ct = CompetitiveTracker("fake-key")
    qd = "test-qd"
    sendingIpAddress = "test-ip"
    endpoint = "/ipdeliverability/%s" % sendingIpAddress
    url = ct.intelligence.ipdeliverability.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.ipdeliverability.get_deliverability_stats(qd=qd, sendingIpAddress=sendingIpAddress)
    assert json_output == 'yay'


@responses.activate
def test_ipdeliverability_get_deliverability_stats_for_range():
    ct = CompetitiveTracker("fake-key")
    qd = "test-qd"
    startingIpAddress = "test-ip"
    endpoint = "/ipdeliverability/range/%s" % startingIpAddress
    url = ct.intelligence.ipdeliverability.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.ipdeliverability.get_deliverability_stats_for_range(startingIpAddress=startingIpAddress, qd=qd)
    assert json_output == 'yay'


@responses.activate
def test_domain_get_average_volume_per_campaign():
    ct = CompetitiveTracker("fake-key")
    qd = "test-qd"
    domain = "test_domain"
    endpoint = "/%s/averageVolumePerCampaign" % domain
    url = ct.intelligence.domain.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.domain.get_average_volume_per_campaign(domain=domain, qd=qd)
    assert json_output == 'yay'


@responses.activate
def test_domain_get_campaigns():
    ct = CompetitiveTracker("fake-key")
    qd = "test-qd"
    domain = "test_domain"
    endpoint = "/%s/campaigns" % domain
    url = ct.intelligence.domain.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.domain.get_campaigns(domain=domain, qd=qd)
    assert json_output == 'yay'


@responses.activate
def test_domain_get_campaigns_per_week():
    ct = CompetitiveTracker("fake-key")
    domain = "test_domain"
    endpoint = "/%s/campaignsPerWeek" % domain
    url = ct.intelligence.domain.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.domain.get_campaigns_per_week(domain=domain)
    assert json_output == 'yay'


@responses.activate
def test_domain_get_dow_avg_volume():
    ct = CompetitiveTracker("fake-key")
    domain = "test_domain"
    endpoint = "/%s/dayOfWeekAverageVolume" % domain
    url = ct.intelligence.domain.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.domain.get_dow_avg_volume(domain=domain)
    assert json_output == 'yay'


@responses.activate
def test_domain_get_isp_placements():
    ct = CompetitiveTracker("fake-key")
    qd = "test-qd"
    domain = "test_domain"
    endpoint = "/%s/ispPlacements" % domain
    url = ct.intelligence.domain.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.domain.get_isp_placements(domain=domain, qd=qd)
    assert json_output == 'yay'


@responses.activate
def test_domain_get_total_volume():
    ct = CompetitiveTracker("fake-key")
    domain = "test_domain"
    endpoint = "/%s/totalVolume" % domain
    url = ct.intelligence.domain.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.domain.get_total_volume(domain=domain)
    assert json_output == 'yay'


@responses.activate
def test_domain_get_volumes():
    ct = CompetitiveTracker("fake-key")
    qd = "test-qd"
    domain = "test_domain"
    endpoint = "/%s/volumes" % domain
    url = ct.intelligence.domain.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.intelligence.domain.get_volumes(domain=domain, qd=qd)
    assert json_output == 'yay'



