import responses
from competitivetracker import CompetitiveTracker


@responses.activate
def test_brands_get_all_brands():
    ct = CompetitiveTracker("fake-key")
    endpoint = ""
    url = ct.core.brands.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.brands.get_all_brands()
    assert json_output == 'yay'


@responses.activate
def test_brands_get_brand_details():
    ct = CompetitiveTracker("fake-key")
    brandId = 1
    endpoint = "/%s" % brandId
    url = ct.core.brands.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.brands.get_brand_details(brandId=brandId)
    assert json_output == 'yay'


@responses.activate
def test_brands_get_all_brand_domains():
    ct = CompetitiveTracker("fake-key")
    brandId = 1
    endpoint = "/%s/domains" % brandId
    url = ct.core.brands.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.brands.get_all_brand_domains(brandId=brandId)
    assert json_output == 'yay'


@responses.activate
def test_companies_get_all_companies():
    ct = CompetitiveTracker("fake-key")
    endpoint = ""
    url = ct.core.companies.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.companies.get_all_companies()
    assert json_output == 'yay'


@responses.activate
def test_companies_get_company_details():
    ct = CompetitiveTracker("fake-key")
    companyId = 1
    endpoint = "/%s" % companyId
    url = ct.core.companies.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.companies.get_company_details(companyId=companyId)
    assert json_output == 'yay'


@responses.activate
def test_companies_get_all_company_brands():
    ct = CompetitiveTracker("fake-key")
    companyId = 1
    endpoint = "/%s/brands" % companyId
    url = ct.core.companies.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.companies.get_all_company_brands(companyId=companyId)
    assert json_output == 'yay'


@responses.activate
def test_discover_search_industries():
    ct = CompetitiveTracker("fake-key")
    search_text = "test"
    endpoint = "/industry"
    url = ct.core.discover.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.discover.search_industries(q=search_text)
    assert json_output == 'yay'


@responses.activate
def test_discover_search_esps():
    ct = CompetitiveTracker("fake-key")
    search_text = "test"
    endpoint = "/esp"
    url = ct.core.discover.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.discover.search_esps(q=search_text)
    assert json_output == 'yay'


@responses.activate
def test_discover_search_brands():
    ct = CompetitiveTracker("fake-key")
    search_text = "test"
    endpoint = "/brand"
    url = ct.core.discover.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.discover.search_brands(q=search_text)
    assert json_output == 'yay'


@responses.activate
def test_discover_search_companies():
    ct = CompetitiveTracker("fake-key")
    search_text = "test"
    endpoint = "/company"
    url = ct.core.discover.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.discover.search_companies(q=search_text)
    assert json_output == 'yay'


@responses.activate
def test_discover_search_domains():
    ct = CompetitiveTracker("fake-key")
    search_text = "test"
    endpoint = "/domain"
    url = ct.core.discover.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.discover.search_domains(q=search_text)
    assert json_output == 'yay'


@responses.activate
def test_discover_search():
    ct = CompetitiveTracker("fake-key")
    search_text = "test"
    endpoint = ""
    url = ct.core.discover.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.discover.search(q=search_text)
    assert json_output == 'yay'


@responses.activate
def test_domains_get_all_domains():
    ct = CompetitiveTracker("fake-key")
    endpoint = "/domains"
    url = ct.core.domains.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.domains.get_all_domains()
    assert json_output == 'yay'


@responses.activate
def test_domains_get_domain_details():
    ct = CompetitiveTracker("fake-key")
    domainId = 1
    endpoint = "/%s" % domainId
    url = ct.core.domains.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.domains.get_domain_details(domainId=domainId)
    assert json_output == 'yay'


@responses.activate
def test_esps_get_all_esps():
    ct = CompetitiveTracker("fake-key")
    endpoint = ""
    url = ct.core.esps.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.esps.get_all_esps()
    assert json_output == 'yay'


@responses.activate
def test_esps_get_esp_details():
    ct = CompetitiveTracker("fake-key")
    espId = 1
    endpoint = "/%s" % espId
    url = ct.core.esps.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.esps.get_esp_details(espId=espId)
    assert json_output == 'yay'


@responses.activate
def test_graph_get_company_from_domain():
    ct = CompetitiveTracker("fake-key")
    domainName = "example"
    endpoint = "/domain/%s" % domainName
    url = ct.core.graph.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.graph.get_company_from_domain(domainName=domainName)
    assert json_output == 'yay'


@responses.activate
def test_graph_get_company():
    ct = CompetitiveTracker("fake-key")
    search_text = "example"
    endpoint = "/company"
    url = ct.core.graph.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.graph.get_company(q=search_text)
    assert json_output == 'yay'


@responses.activate
def test_graph_get_company_from_id():
    ct = CompetitiveTracker("fake-key")
    companyId = 1
    endpoint = "/company/%s" % companyId
    url = ct.core.graph.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.graph.get_company_from_id(companyId=companyId)
    assert json_output == 'yay'


@responses.activate
def test_industries_get_all_industries():
    ct = CompetitiveTracker("fake-key")
    endpoint = ""
    url = ct.core.industries.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.industries.get_all_industries()
    assert json_output == 'yay'

@responses.activate
def test_industries_get_industry_details():
    ct = CompetitiveTracker("fake-key")
    industryId = 1
    endpoint = "/%s" % industryId
    url = ct.core.industries.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.industries.get_industry_details(industryId=industryId)
    assert json_output == 'yay'

@responses.activate
def test_industries_get_all_industry_brands():
    ct = CompetitiveTracker("fake-key")
    industryId = 1
    endpoint = "/%s/brands" % industryId
    url = ct.core.industries.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    json_output = ct.core.industries.get_all_industry_brands(industryId=industryId)
    assert json_output == 'yay'

@responses.activate
def test_ping_ping_service():
    ct = CompetitiveTracker("fake-key")
    endpoint = ""
    url = ct.core.ping.uri + endpoint
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body='{"results": "pong"}'
    )
    output = ct.core.ping.ping_service()
    assert output == "pong"