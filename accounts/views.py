from django.contrib.auth import user_logged_in
from django.contrib.auth import user_logged_out
from rest_framework import generics
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from accounts import serializers
from accounts.models import User
from helpers.email import EmailMixin


class UserView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    model = User
    serializer_class = serializers.UserSerializers
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset


class UserRegistration(EmailMixin, generics.CreateAPIView):
    serializer_class = serializers.RegistrationSerializers
    permission_classes = (
         permissions.AllowAny,
    )

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = True
        user.save()

class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def finalize_response(self, request, *args, **kwargs):
        response_obj = super(LoginView, self).finalize_response(
            request, *args, **kwargs)
        if request.POST and response_obj.status_code == 200:
            response_obj['Authorization'] = 'Token ' \
                                            + response_obj.data['auth_token']
            response_obj.set_cookie(
                'Authorization', response_obj['Authorization'])
        return response_obj

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            user_logged_in.send(
                sender=user.__class__, request=self.request, user=user)
            return response.Response(
                data=serializers.TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

class LogoutView(views.APIView):

    """
    Use this endpoint to logout user (remove user authentication token).
    """
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def finalize_response(self, request, *args, **kwargs):
        response_obj = super(LogoutView, self).finalize_response(
            request, *args, **kwargs)
        if request.method == "POST":
            response_obj['Authorization'] = None
            response_obj.delete_cookie('Authorization')
        return response_obj

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        user_logged_out.send(
            sender=request.user.__class__,
            request=request,
            user=request.user)
        return response.Response(status=status.HTTP_200_OK)