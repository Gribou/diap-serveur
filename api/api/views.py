from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT


class HealthCheckView(APIView):
    '''
    Vérification que le serveur web est en route
    A utiliser avec Docker-compose pour établir l'état de santé du container
    (healthcheck)
    '''

    def get(self, request, format=None):
        return Response(status=HTTP_204_NO_CONTENT)
