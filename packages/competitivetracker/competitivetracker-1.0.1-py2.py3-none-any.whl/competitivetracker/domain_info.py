from .base import Resource
import json
import requests

param_model = {
    'domain',
    'endDate',
    'mustMatchTLD',
    'precision',
    'timePeriod'
    }

class Domain_Info(Resource):
    key = "domain_info"

    def get_domain_info(self, **kwargs):
        """
        Determines the sending list size, recent ESPs, and personalization information for domains.

        :param domain:  List of strings.  Domain to find info for (multiple allowed)

        :return:  A ``list`` of object ``dict`` containing sending list and ESP details for a domain
        """

        endpoint = ""
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse

    def get_brand_volume_and_esps(self, domains, **kwargs):
        """
        Returns the average sending volume of a list of brands over a user defined time period (average can be per
        month or per day) and every ESPs from domains associated with the brand.

        :param domains:  List of strings.  Domains to find info for (multiple allowed)
        :param str endDate:  Endpoint of the requested date range concerning volume data with a format of yyyy-mm-dd.
            This date is exclusive: data concerning the given date will not be included in volume average.

            Defaults to current date
        :param str precision:  Precision of the average (i.e. per month or per day).

            Accepts: ``days`` or ``months``.

            Defaults to ``days``.

        :param int timePeriod:  How many days or months back you would like sending volume data for.  This is for a
            time period backwards.

            Defaults to ``30``.

        :param bool mustMatchTLD:  Include only domains that match the top level domain (TLD) of any domain requested

        :return:  A ``dict`` object where each element is a ``list`` of ``dict`` containing average sending volumes
            for brands
        """

        if len(domains) < 300:
            endpoint = "/brand_volume_average_and_esps"
            apiUrl = self.uri + endpoint
            parameters = self.SetParameters(kwargs, param_model)
            parameters["domain"] = domains
            apiResponse = self.request("GET", apiUrl, params=parameters)
        else:
            endpoint = "/brand_volume_average_and_esps"
            apiUrl = self.uri + endpoint
            parameters = self.SetParameters(kwargs, param_model)
            apiResponse = self.request("POST", apiUrl, params=parameters, json=domains)

        return apiResponse
