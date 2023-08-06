from .base import Resource

param_model = {
    'domain',
    'embed',
    'excludeSameCompany',
    'ignoreIndustry',
    'maxResults',
    'minThreshold',
    'overlapDomain',
    'qd'
}

class Overlaps(Resource):
    key = "overlaps"

    def get_domain_overlaps(self, domain, **kwargs):
        """
        Determines the overlap for a domain given the filters specified.

        :param str domain:  (Required) The domain to use in the request
        :param int minThreshold:  Minimum overlap percentage to use

            Defaults to ``10``

        :param int maxResults:  Maximum Results to return

            Defaults to ``100``

        :param bool ignoreIndustry:  If you wish to ignore the industry filter and return all overlaps

            Defaults to ``False``

        :param bool excludeSameCompany:  If you wish to exclude domains that are under the same company

            Defaults to ``False``

        :param str embed:  The objects within the return model you wish to embed in the form of
            'customer, customer.name, etc'

            Accepts:  ``readRatePercent``, ``projectedReach``

        :return:  A ``dict`` containing overlap details.
        """
        endpoint = "/%s" % domain
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_narrowed_overlap(self, domain, **kwargs):
        """
        Determines the overlap for a domain against a specific set and include attributes about the overlap.

        :param str domain:  (Required) The domain to use in the request
        :param overlapDomain:  (Required) List of strings.  The other domains to analyze overlap with (multiple params
            accepted)

        :return:  A ``dict`` containing overlap details.
        """
        endpoint = "/narrow/%s" % domain
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_top_competing(self, domain, **kwargs):
        """
        Determines the top competing domains and returns their overlaps.

        :param str domain:  (Required) The domain to use in the request
        :param int minThreshold:  Minimum overlap percentage to use

            Defaults to ``10``

        :param int maxResults:  Maximum Results to return

            Defaults to ``100``

        :param str embed:  The objects within the return model you wish to embed in the form of
            'customer, customer.name, etc'

            Accepts:  ``readRatePercent``, ``projectedReach``

        :return:  A ``dict`` containing overlap details
        """
        endpoint = "/%s/top_competing" % domain
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse
