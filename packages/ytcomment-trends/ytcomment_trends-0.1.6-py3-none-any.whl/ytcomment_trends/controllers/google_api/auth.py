import googleapiclient.discovery

class GoogleAPIAuth:
    """Google API OAuth2.0 authentication class
    """

    def __init__(self, api_key):
        self.API_SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.API_KEY = api_key

    def get_authenticated_service(self):
        """Initialize Google Auth service

        Returns:
            googleapiclient object
        """
        return googleapiclient.discovery.build(self.API_SERVICE_NAME, self.API_VERSION, developerKey=self.API_KEY)