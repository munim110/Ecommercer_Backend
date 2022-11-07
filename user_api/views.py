from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import viewsets

from user_api.models import SiteUser
from user_api.serializers import *
import logging

# Create your views here.

class UserViewset(viewsets.ModelViewSet):
    queryset = SiteUser.objects.all()
    serializer_class = UserSerializer

class UserObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        checkUser = SiteUser.objects.filter(username=username)
        
        if not checkUser:
            return Response({'non_field_errors': 'User does not exist'})
        
        response = super(UserObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = SiteUser.objects.get(id=token.user_id)
        userSerializer = UserSerializer(user)
        return Response({'token': token.key, 'user': userSerializer.data})
    
class ChangePasswordView(viewsets.ModelViewSet):
    serializer_class = ChangePasswordSerializer
    
    def update(self, request, pk=None):
        user = SiteUser.objects.get(id=pk)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            logging.warning(serializer.data)
            if not user.check_password(serializer.data['old_password']):
                return Response({'result': 'Old password is incorrect'})
            user.set_password(serializer.data['new_password'])
            user.save()
            return Response({'result': 'success'})
        return Response({'result': 'failure'})