from .user import UsersApi, UserApi
from .geo import GeoRequest, AIRequest, SHPFile

##Routes for the classes and methods
def initialize_routes(api):
    api.add_resource(UsersApi, '/api/users/')
    api.add_resource(UserApi, '/api/users/results/')
    api.add_resource(GeoRequest, '/api/geo/')
    api.add_resource( AIRequest, '/api/geoAI/')
    api.add_resource(SHPFile, '/api/sendFile/')

