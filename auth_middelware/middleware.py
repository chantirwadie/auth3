from django.conf import settings
from .jwtHandler import  handleJwtVerification
import json
import logging
from django.http import HttpResponse, JsonResponse
from core.serializers import UserSerializer
from django.contrib.auth import get_user

logger = logging.getLogger(__name__)


def check_string(path, list):
    for item in list:
        if path.startswith(item):
            return True
    return False

def create_response(request_id, code, message):

    """
    Function to create a response to be sent back via the API
    :param request_id:Id fo the request
    :param code:Error Code to be used
    :param message:Message to be sent via the APi
    :return:Dict with the above given params
    """

    try:
        req = str(request_id)
        data = {"data": message, "code": int(code), "request_id": req}
        return data
    except Exception as creation_error:
        logger.error(f'create_response:{creation_error}')

class AuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.accessToken = ""
        self.user = None

    def __call__(self, request):
        _response = self.process_request(request)
        response = self.get_response(request)
        if _response:
            return _response
        return response 

    def process_request(self, request):

        # The list of URLs to exclude from this middelware verification
        exclusion_list = settings.EXCLUSION_LIST

        if  not check_string(request.path, exclusion_list):

            # Extracting the access token from the authorization header
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]

            if token:
                try: 
                    (user , access_token) = handleJwtVerification(token, request)
                    self.user = user
                    self.accessToken = access_token
                    request.session['user'] = UserSerializer(user).data
                    return None
                except:
                    response = create_response(
                    "", 401, {"message": "Refresh token is invalid or expired"}
                    )
                    logger.info(f"Response {response}")
                    response = JsonResponse(response)
                    response.status_code = 401
                    return response 

            else:
                response = create_response("", 401, {"message": "Access token is invalid or expired"})
                logger.info(f"Response {response}")
                response = JsonResponse(response)
                response.status_code = 401
                return response 
        else:
            return None 

    def process_template_response(self,request, response):
        if self.user:
            request.user = self.user
        accessToken = self.accessToken
        if(accessToken):
            response.data["access_token"] = accessToken
        return response                     




    