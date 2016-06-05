import requests


class Localytics:
    def __init__(self):
        self.api_root = 'https://profile.localytics.com/v1/profiles'

    def track_profile(self, customer_id, attributes={}):
        url = "%s/%s" % (self.api_root, customer_id)
        return requests.patch(url, json={'attributes': attributes},
                              auth=(self.api_key, self.api_secret))

    def init_app(self, app):
        self.app = app
        self.api_key = app.config['LOCALYTICS_API_KEY']
        self.api_secret = app.config['LOCALYTICS_API_SECRET']

localytics = Localytics()
