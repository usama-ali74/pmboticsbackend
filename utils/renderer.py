import json

from rest_framework import renderers


class CustomRenderer(renderers.BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, response_status):
        print(response_status)
        print(data)

        return {}