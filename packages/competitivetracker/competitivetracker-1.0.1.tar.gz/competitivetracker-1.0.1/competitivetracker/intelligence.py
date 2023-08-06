from .base import Resource

param_model = {
    'brandId',
    'campaignId',
    'campaignLengthFilter',
    'domain',
    'embed',
    'lastBlock',
    'order',
    'page',
    'per_page',
    'qd',
    'sendingIpAddress',
    'startDate',
    'startingIpAddress',
    'weeksBack'
}

class Intelligence:

    def __init__(self, base_uri, api_key):
        self.domain = Domain(base_uri, api_key)
        self.brand = Brand(base_uri, api_key)
        self.campaign = Campaign(base_uri, api_key)
        self.ipdeliverability = IpDeliverability(base_uri, api_key)


class Brand(Resource):
    key = "intelligence"

    def get_top_domains(self, brandId, **kwargs):
        """
        Find sending volumes (commercial and non-commercial) within the past 30 days, for a given Brand.

        :param int brandId:  (Required) The Brand ID to get top sending domains for

        :return:  A ``list`` of object ``dict`` containing top domains and volume details.
        """
        endpoint = "/brand/%s/top_domains" % brandId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse


class Campaign(Resource):
    key = "intelligence"

    def get_target_country(self, campaignId, **kwargs):
        """
        Returns (or evaluates from scratch, for historical campaigns) the likely target country in the form of an
        ISO 3166-1 alpha-2 String.  (Examples: ``US``, ``CA``, ``MX``).

        :param int campaignId:  (Required) The id of the campaign you wish to evaluate.

        :return:  A ``dict`` object containing likely target country.
        """
        endpoint = "/campaign/targetCountry/%s" % campaignId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_campaign(self, campaignId, **kwargs):
        """
        Gets a campaign by id if found.  Detected sending or forwarding IPs are accessible via the sendingIps
        embed option.

        :param int campaignId: (Required) The id of the campaign you wish to evaluate
        :param str embed:  The objects within the return model you wish to embed in the
            form of 'customer, customer.name, etc'

            Accepts:  ``sendingIps``, ``rawEmail``, ``ispPlacements``, ``links``, ``headers`` (headers is
            only available for ESP-owned accounts).

        :return:  A ``dict`` object containing campaign details.
        """
        endpoint = "/campaign/%s" % campaignId
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse


class Domain(Resource):
    key = "intelligence"

    def get_campaigns(self, domain, **kwargs):
        """
        Search for campaigns from a certain sending domain.  Detected sending or forwarding IPs are accessible via
        the sendingIps embed option.

        :param str domain:  (Required) The domain to use in the request
        :param str qd:  (Required) A date range query parameter.

            Accepts:  ``since:YYYYMMDD``, ``between:YYYYMMDDhhmmss,YYYYMMDDhhmmss``, and ``daysBack:N``.

            Examples:  ``since:20190601``, ``between:20191001000000,20191002060000``, ``daysBack:30``

        :param str campaignLengthFilter:  Length filter in days for the campaign

            Examples: ``>,2``, ``<,5``, ``=,1``
        :param int page:  The page to query for in pagination
        :param int per_page:  The amount of records per page you wish to query for (max 100)
        :param str order:  The property to sort by ('property' for descending, '-property' for ascending)

            Accepts:  ``firstSeen``, ``-firstSeen``, ``lastSeen``, ``-lastSeen``, ``inbox``, ``-inbox``, ``spam``,
            ``-spam``

        :param str embed:  The objects within the return model you wish to embed in the form of
            'customer,customer.name,etc'

            Accepts:  ``sendingIps``, ``rawEmail``, ``ispPlacements``, ``links``, ``headers`` (headers is only
            available for ESP-owned accounts).

        :return:  A ``list`` of object ``dict`` containing campaign details.
        """
        endpoint = "/%s/campaigns" % domain
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_campaigns_per_week(self, domain, **kwargs):
        """
        Find the campaign average per week for given domain

        :param str domain:  (Required) The domain to use in the request
        :param str startDate:  Start date for the query.  Formatted as ``YYYYMMDD``

            Defaults to now.

        :param int weeksBack:  How many weeks to look back prior to startDate or now

            Defaults to ``4``

        :return:  A ``str`` of average campaigns
        """
        endpoint = "/%s/campaignsPerWeek" % domain
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_average_volume_per_campaign(self, domain, **kwargs):
        """
        Find the average campaign volume for a domain over a given time period

        :param str domain:  (Required) The domain to use in the request
        :param str qd:  A date range query parameter.

            Accepts:  ``since:YYYYMMDD``, ``between:YYYYMMDDhhmmss,YYYYMMDDhhmmss``, and ``daysBack:N``.

            Examples:  ``since:20190601``, ``between:20191001000000,20191002060000``, ``daysBack:30``

            Defaults to ``daysBack:28``

        :return:  A ``str`` of average campaign volume
        """
        endpoint = "/%s/averageVolumePerCampaign" % domain
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_volumes(self, domain, **kwargs):
        """
        Find sending volumes (commercial and non-commercial) within a period, for a given domain.  Collected into
        date groups based on days in date range: "DAY" for 31 days and less, "WEEK" for 182 days and less,
        "MONTH" for greater than 182 days.

        :param str domain:  (Required) The domain to use in the request
        :param str qd:  (Required) A date range query parameter.

            Accepts:  ``since:YYYYMMDD``, ``between:YYYYMMDDhhmmss,YYYYMMDDhhmmss``, and ``daysBack:N``.

            Examples:  ``since:20190601``, ``between:20191001000000,20191002060000``, ``daysBack:30``

        :param str embed:  The objects within the return model you wish to embed in the form of
            'customer, customer.name, etc'

            Accepts:  ``ispPlacements``

        :return:  A ``list`` of object ``dict`` containing sending volume details
        """
        endpoint = "/%s/volumes" % domain
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_isp_placements(self, domain, **kwargs):
        """
        Find ISP placements statistics within a date for a given domain

        :param str domain:  (Required) The domain to use in the request
        :param str qd:  (Required) A date range query parameter.

            Accepts:  ``since:YYYYMMDD``, ``between:YYYYMMDDhhmmss,YYYYMMDDhhmmss``, and ``daysBack:N``.

            Examples:  ``since:20190601``, ``between:20191001000000,20191002060000``, ``daysBack:30``

        :return:  A ``list`` of object ``dict`` containing ISP deliverability metrics.
        """
        endpoint = "/%s/ispPlacements" % domain
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_dow_avg_volume(self, domain, **kwargs):
        """
        Find average sending volumes (commercial and non-commercial) broken down by day of week within a date for
        a given domain.

        :param str domain:  (Required) The domain to use in the request
        :param str qd:  A date range query parameter.

            Accepts:  ``since:YYYYMMDD``, ``between:YYYYMMDDhhmmss,YYYYMMDDhhmmss``, and ``daysBack:N``.

            Examples:  ``since:20190601``, ``between:20191001000000,20191002060000``, ``daysBack:30``

            Defaults to ``daysBack:30``

        :param str embed:  The objects within the return model you wish to embed in the form of
            'customer, customer.name, etc'

            Accepts: ``ispPlacements``

        :return:  A ``list`` of object ``dict`` containing volume details.
        """
        endpoint = "/%s/dayOfWeekAverageVolume" % domain
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_total_volume(self, domain, **kwargs):
        """
        Find the total sending volume (commercial and non-commercial) within a date for a given domain.

        :param str domain:  (Required) The domain to use in the request
        :param str qd:  A date range query parameter.

            Accepts:  ``since:YYYYMMDD``, ``between:YYYYMMDDhhmmss,YYYYMMDDhhmmss``, and ``daysBack:N``.

            Examples:  ``since:20190601``, ``between:20191001000000,20191002060000``, ``daysBack:30``

            Defaults to ``daysBack:30``

        :param str embed:  The objects within the return model you wish to embed in the form of
            'customer, customer.name, etc'

            Accepts:  ``ispPlacements``

        :return:  A ``dict`` containing volume details
        """
        endpoint = "/%s/totalVolume" % domain
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse



class IpDeliverability(Resource):
    key = "intelligence"

    def get_deliverability_stats(self, sendingIpAddress, **kwargs):
        """
        Get the IP deliverability statistics (only commercial) for a sending IP address, and the specified filters

        :param str sendingIpAddress:  (Required) The ip address to view results for.
        :param str qd:  (Required) A date range query parameter.

            Accepts:  ``since:YYYYMMDD``, ``between:YYYYMMDDhhmmss,YYYYMMDDhhmmss``, and ``daysBack:N``.

            Examples:  ``since:20190601``, ``between:20191001000000,20191002060000``, ``daysBack:30``

        :return:  A ``dict`` object containing deliverability stats.
        """
        endpoint = "/ipdeliverability/%s" % sendingIpAddress
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_deliverability_stats_for_range(self, startingIpAddress, **kwargs):
        """
        Get the per-IP deliverability statistics (only commercial) for a range of sending IP addresses,
        and the specified filters

        :param str startingIpAddress:  (Required) The starting ip address to view results for
        :param str qd:  (Required) A date range query parameter.

            Accepts:  ``since:YYYYMMDD``, ``between:YYYYMMDDhhmmss,YYYYMMDDhhmmss``, and ``daysBack:N``.

            Examples:  ``since:20190601``, ``between:20191001000000,20191002060000``, ``daysBack:30``

        :param str lastBlock:  The last block of the range to request (last octet for IPv4 or last hextet in IPv6,
            max 256 return IPs)

        :return:  A ``list`` of object ``dict`` containing deliverability and reputation stats.
        """
        endpoint = "/ipdeliverability/range/%s" % startingIpAddress
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_agg_stats_for_range(self, startingIpAddress, **kwargs):
        """
        Get the aggregate deliverability statistics (only commercial) for a range of sending IP addresses,
        and the specified filters.

        :param str startingIpAddress:  (Required) The starting ip address to view results for

        :param str qd:  (Required) A date range query parameter.

            Accepts:  ``since:YYYYMMDD``, ``between:YYYYMMDDhhmmss,YYYYMMDDhhmmss``, and ``daysBack:N``.

            Examples:  ``since:20190601``, ``between:20191001000000,20191002060000``, ``daysBack:30``

        :param str lastBlock:  The last block of the range to request (last octet for
            IPv4 or last hextet in IPv6, max 256 return IPs)

        :param str embed:  The objects within the return model you wish to embed in the form of 'customer,
            customer.name, etc'

            Accepts:  ``ispPlacements``

        :return:  A ``dict`` object containing deliverability and volume details.
        """
        endpoint = "/ipdeliverability/range/%s/totalVolume" % startingIpAddress
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse


