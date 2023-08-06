from .base import Resource

param_model = {
}


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
