from .base import Resource

param_model = {
    'embed',
    'order',
    'page',
    'per_page',
    'q'
}


class Core:

    def __init__(self, base_uri, api_key):
        self.brands = Brands(base_uri, api_key)
        self.companies = Companies(base_uri, api_key)
        self.discover = Discover(base_uri, api_key)
        self.domains = Domains(base_uri, api_key)
        self.esps = Esps(base_uri, api_key)
        self.graph = Graph(base_uri, api_key)
        self.industries = Industries(base_uri, api_key)
        self.ping = Ping(base_uri, api_key)


class Industries(Resource):
    key = "industries"

    def get_all_industries(self, **kwargs):
        """
        Returns all of the industries ordered by name (paged).

        :param int page:  The page to query for in pagination
        :param int per_page:  The amount of records per page you wish to query for (max 100)
        :param str order:  The property to sort by ('property' for descending, '-property' for ascending)

            Accepts:  ``name``, ``-name``

        :return:  A ``list`` of object ``dict`` containing name and id of all industries
        """
        endpoint = ""
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_industry_details(self, industryId, **kwargs):
        """
        Get a distinct industry by its id.

        :param int industryId:  The id of the industry

        :return:  A ``dict`` containing name and id
        """
        endpoint = "/%s" % industryId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_all_industry_brands(self, industryId, **kwargs):
        """
        All the brands associated with an industry.

        :param int industryId:  The id of the industry
        :param int page:  The page to query for in pagination
        :param int per_page:  The amount of records per page you wish to query for (max 100)
        :param str order:  The property to sort by ('property' for descending, '-property' for ascending)

            Accepts:  ``name``, ``-name``

        :return:  A ``list`` of object ``dict`` containing matching results, with name and id
        """
        endpoint = "/%s/brands" % industryId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse


class Esps(Resource):
    key = "esps"

    def get_all_esps(self, **kwargs):
        """
        Returns all of the email service providers ordered by name (paged).

        :param int page:  The page to query for in pagination
        :param int per_page:  The amount of records per page you wish to query for (max 100)
        :param str order:  The property to sort by ('property' for descending, '-property' for ascending)

            Accepts:  ``name``, ``-name``

        :return:  A ``list`` of object ``dict`` containing name and id of all esps
        """
        endpoint = ""
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_esp_details(self, espId, **kwargs):
        """
        Get a distinct ESP by its ID.

        :param int espId:  The ID of the ESP

        :return:  A ``dict`` containing name and id
        """
        endpoint = "/%s" % espId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse


class Discover(Resource):
    key = "discover"

    def search_industries(self, **kwargs):
        """
        Search in industries for a matching string (max 1000 results).

        :param str q:  Query parameter to match.  String to search for.

        :return:  A ``dict`` containing name and id of search results
        """
        endpoint = "/industry"
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def search_esps(self, **kwargs):
        """
        Search ESPs for a matching string (max 1000 results).

        :param str q:  Query parameter to match.  String to search for.

        :return:  A ``dict`` containing name and id of search results
        """
        endpoint = "/esp"
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def search_brands(self, **kwargs):
        """
        Search in brands for a matching string (max 1000 results).

        :param str q:  Query parameter to match.  String to search for.

        :return:  A ``dict`` containing name and id of search results
        """
        endpoint = "/brand"
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def search_companies(self, **kwargs):
        """
        Search in companies for a matching string (max 1000 results).

        :param str q:  Query parameter to match.  String to search for.

        :return:  A ``dict`` containing name and id of search results
        """
        endpoint = "/company"
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def search_domains(self, **kwargs):
        """
        Search in domains for a matching string (max 1000 results).

        :param str q:  Query parameter to match.  String to search for.

        :return:  A ``dict`` containing name and id of search results
        """
        endpoint = "/domain"
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def search(self, **kwargs):
        """
        Search in all the core types for a matching string (max 1000 results).

        :param str q:  Query parameter to match.  String to search for.

        :return:  A ``dict`` containing name and id of search results
        """
        endpoint = ""
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse


class Brands(Resource):
    key = "brands"

    def get_all_brands(self, **kwargs):
        """
        Returns all of the brands (paged).

        :param int page:  The page to query for in pagination
        :param int per_page:  The amount of records per page you wish to query for (max 100)
        :param str order:  The property to sort by ('property' for descending, '-property' for ascending)

            Accepts:  ``name``, ``-name``

        :param str embed:  The objects within the return model you wish to embed in the form of
            'customer, customer.name, etc'

            Accepts:  ``address``, ``company``, ``industry``

        :return:  A ``list`` of object ``dict`` containing name and id of all brands
        """
        endpoint = ""
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_brand_details(self, brandId, **kwargs):
        """
        Get a distinct brand by its id.

        :param int brandId:  The id of the brand

        :return:  A ``dict`` containing name and id
        """
        endpoint = "/%s" % brandId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_all_brand_domains(self, brandId, **kwargs):
        """
        All the domains associated with the brand.

        :param int brandId:  The id of the brand
        :param int page:  The page to query for in pagination
        :param int per_page:  The amount of records per page you wish to query for (max 100)
        :param str order:  The property to sort by ('property' for descending, '-property' for ascending)

            Accepts:  ``name``, ``-name``

        :return:  A ``list`` of object ``dict`` containing matching results, with name and id
        """
        endpoint = "/%s/domains" % brandId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse


class Companies(Resource):
    key = "companies"

    def get_all_companies(self, **kwargs):
        """
        Returns all of the companies (paged).

        :param int page:  The page to query for in pagination
        :param int per_page:  The amount of records per page you wish to query for (max 100)
        :param str order:  The property to sort by ('property' for descending, '-property' for ascending)

            Accepts:  ``name``, ``-name``

        :param str embed:  The objects within the return model you wish to embed in the form of
            'customer, customer.name, etc'

            Accepts:  ``address``, ``company``, ``industry``

        :return:  A ``list`` of object ``dict`` containing name and id of all companies
        """
        endpoint = ""
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_company_details(self, companyId, **kwargs):
        """
        Get a distinct company by its id.

        :param int companyId:  The id of the company

        :return:  A ``dict`` containing name and id
        """
        endpoint = "/%s" % companyId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_all_company_brands(self, companyId, **kwargs):
        """
        All the brands associated with the company.

        :param int companyId:  The id of the company
        :param int page:  The page to query for in pagination
        :param int per_page:  The amount of records per page you wish to query for (max 100)
        :param str order:  The property to sort by ('property' for descending, '-property' for ascending)

            Accepts:  ``name``, ``-name``

        :return:  A ``list`` of object ``dict`` containing matching results, with name and id
        """
        endpoint = "/%s/brands" % companyId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse


class Domains(Resource):
    key = "domains"

    def get_all_domains(self, **kwargs):
        """
        Returns all of the domains (paged).

        :param str page:  The page to query for in pagination
        :param str per_page:  The amount of records per page you wish to query for (max 100)
        :param str order:  The property to sort by ('property' for descending, '-property' for ascending)

            Accepts:  ``name``, ``-name``

        :return:  A ``list`` of object ``dict`` containing name and id of all companies
        """
        endpoint = "/domains"
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_domain_details(self, domainId, **kwargs):
        """
        Get a distinct domain by its id.

        :param int domainId:  The id of the domain
        :param str embed:  The objects within the return model you wish to embed in the form of
            'customer,customer.name,etc'

            Accepts:  ``brands``, ``brands.address``, ``brands.company``, ``brands.industry``

        :return:  A ``dict`` containing name and id
        """
        endpoint = "/%s" % domainId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse


class Graph(Resource):
    key = "graph"

    def get_company_from_domain(self, domainName, **kwargs):
        """
        Get the company the domain belongs to and display the graph.

        :param str domainName:  The name of the domain under the company.

        :return:  A ``dict`` containing company details
        """
        endpoint = "/domain/%s" % domainName
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_company(self, **kwargs):
        """
        Get the company graphs by searching for company names.

        :param str q:  The string to search with (at least 3 characters)

        :return:  A ``list`` of object ``dict`` containing company details
        """
        endpoint = "/company"
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_company_from_id(self, companyId, **kwargs):
        """
        Get the company graph for a distinct company by its id.

        :param int companyId:  The id of the company

        :return:  A ``dict`` containing company details
        """
        endpoint = "/company/%s" % companyId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse


class Ping(Resource):
    key = "ping"

    def ping_service(self):
        """
        Ping the service to verify it is reachable.

        :return:  A ``str`` object.  A successful ping will return the string 'pong'.
        """
        endpoint = ""
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters({}, {})
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse
