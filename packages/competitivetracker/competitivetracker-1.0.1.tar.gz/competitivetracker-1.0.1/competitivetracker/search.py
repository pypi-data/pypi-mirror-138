from .base import Resource

param_model = {
    'subject',
    'body',
    'campaignLengthFilter',
    'sendingDomain',
    'excludeSendingDomain',
    'brandId',
    'excludedBrandId',
    'companyId',
    'excludedCompanyId',
    'industryId',
    'sentFrom',
    'fromAddress',
    'headerKey',
    'headerValue',
    'receivedUsingMta',
    'mobileReady',
    'hasCreative',
    'onlyCommercial',
    'emojiPresent',
    'readPercentage',
    'readDeletedPercentage',
    'deletedPercentage',
    'inboxPercentage',
    'spamPercentage',
    'projectedVolumeFilter',
    'secondaryProjectedVolumeFilter',
    'droveTrafficToDomain',
    'sendFromIp',
    'espId',
    'espStartIp',
    'espEndIp',
    'espRedirectDomain',
    'espRedirectString',
    'campaignTargetCountry',
    'excludedCampaignTargetCountry',
    'page',
    'per_page',
    'qd',
    'order',
    'embed'
}

class Search(Resource):
    key = "search"

    def search(self, **kwargs):
        """
        Search for campaigns with many different criteria.  Detected sending or forwarding IPs are accessible via the
        sendingIps embed option.

        :param str qd:  (Required) A date range query parameter.

            Accepts:  ``since:YYYYMMDD``, ``between:YYYYMMDDhhmmss,YYYYMMDDhhmmss``, and ``daysBack:N``.

            Examples:  ``since:20190601``, ``between:20191001000000,20191002060000``, ``daysBack:30``

        :param str subject:  Subject search criteria
        :param str body:  Body search criteriaSubject search criteria
        :param str campaignLengthFilter:  Length filter in days for the campaign

            Examples: ``>,2``, ``<,5``, ``=,1``

        :param sendingDomain:  List of strings.  Filter search to specific sending domains (multiple allowed)
        :param excludeSendingDomain:  List of strings.  Filter out specific sending domains (multiple allowed)
        :param brandId:  List of int.  Filter search to specific brands (multiple allowed)
        :param excludedBrandId:  List of int.  Filter out specific brands (multiple allowed)
        :param companyId:  List of int.  Filter search to specific companies (multiple allowed)
        :param excludedCompanyId:  List of int.  Filter out specific companies (multiple allowed)
        :param industryId:  List of int.  Filter search to specific industries (multiple allowed)
        :param str sentFrom:  Campaigns with a matching sent from address
        :param fromAddress:  List of strings.  Campaigns with certain from addresses (multiple allowed)
        :param str headerKey:  Campaigns that used a specific header key
        :param str headerValue:  Campaigns that used a specific header value
        :param str receivedUsingMta:  Campaigns were received using a matched MTA
        :param bool mobileReady:  Campaigns with/without mobile ready format
        :param bool hasCreative:  Campaigns with/without creatives

        :param bool onlyCommercial:  ``True`` for commercial campaigns, ``False`` for daily low-volume rollups,
            and leave unset (null) for both

        :param bool emojiPresent:  Campaigns with/without emojis in the subject
        :param str readPercentage:  Read percentage filter

            Examples: ``>,20``, ``<,5``, ``=,2``
        :param str readDeletedPercentage:  Read+Deleted percentage filter

            Examples: ``>,20``, ``<,5``, ``=,2``
        :param str deletedPercentage:  Deleted percentage filter

            Examples: ``>,20``, ``<,5``, ``=,2``
        :param str inboxPercentage:  Inbox percentage filter

            Examples: ``>,20``, ``<,5``, ``=,2``
        :param str spamPercentage:  Spam percentage filter

            Examples: ``>,20``, ``<,5``, ``=,2``
        :param str projectedVolumeFilter:  Projected Total Volume filter

            Examples: ``>,2000000``, ``<,50000``, ``=,324541``

        :param str secondaryProjectedVolumeFilter:  Secondary Projected Total Volume filter

            Examples:  ``>,2000000``, ``<,50000``, ``=,324541``

        :param droveTrafficToDomain:  List of strings.  Filter search to campaigns that drive traffic to certain domains
            (multiple allowed)

        :param sendFromIp:  List of strings.  Filter search to campaigns that were sent from certain ips
            (multiple allowed)

        :param int espId:  Filter search to a specific ESP
        :param str espStartIp:  The start IP of the sending ESP
        :param str espEndIp:  The end IP of the sending ESP
        :param str espRedirectDomain:  The redirect domain of the sending ESP
        :param str espRedirectString:  The match the redirect string of the sending ESP

        :param campaignTargetCountry:  List of strings.  Filter search to campaigns with a specific target country code
            (multiple allowed)

        :param excludedCampaignTargetCountry:  List of strings.  Filter out campaigns with a specific target country
            code (multiple allowed)

        :param int page:  The page to query for in pagination
        :param int per_page:  The amount of records per page you wish to query for (max 100)
        :param str order:  The property to sort by ('property' for descending, '-property' for ascending)

            Accepts:  ``firstSeen``, ``-firstSeen``, ``lastSeen``, ``-lastSeen``, ``inbox``, ``-inbox``, ``spam``,
            ``-spam``

        :param str embed:  The objects within the return model you wish to embed in the form of
            'customer, customer.name, etc'

            Accepts:  ``sendingIps``, ``rawEmail``, ``ispPlacements``, ``links``, ``headers`` (headers is only available
            for ESP-owned accounts).

        :return:  A ``list`` of object ``dict`` containing campaign details.
        """
        endpoint = ""
        apiUrl = self.uri + endpoint
        parameters = self.SetParameters(kwargs, param_model)
        apiResponse = self.request("GET", apiUrl, params=parameters)

        return apiResponse
