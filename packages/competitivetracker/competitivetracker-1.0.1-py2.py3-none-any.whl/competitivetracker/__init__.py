from .domain_info import Domain_Info
from .intelligence import Brand, Campaign, IpDeliverability, Intelligence  # , Domain
from .overlaps import Overlaps
from .ping import Ping
from .search import Search
from .core import Core


__version__ = '1.0.1'
competitive_tracker_uri = "api.edatasource.com"

competitive_module = '/competitive'
core_module = '/core'


class CompetitiveTracker(object):

    def __init__(self, api_key, base_uri=competitive_tracker_uri, version="4"):

        self.base_uri = 'http://' + base_uri + '/v' + version
        self.api_key = api_key
        self.domain_info = Domain_Info(self.base_uri + competitive_module, self.api_key)
        self.intelligence = Intelligence(self.base_uri + competitive_module, self.api_key)
        self.overlaps = Overlaps(self.base_uri + competitive_module, self.api_key)
        self.ping = Ping(self.base_uri + competitive_module, self.api_key)
        self.search = Search(self.base_uri + competitive_module, self.api_key)
        self.core = Core(self.base_uri + core_module, self.api_key)
