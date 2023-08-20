import time

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Profile
from .serializers import UserProfileSerializer
from .service import generate_invite_code, generate_auth_code


class UserProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        phone = request.POST.get('phone')
        user, created = Profile.objects.get_or_create(phone=phone)

        if created:
            time.sleep(1)
            auth_code = generate_auth_code()
            user.auth_code = auth_code
            user.invite_code = generate_invite_code()
            user.save()
            return Response({'auth_code': auth_code}, status=status.HTTP_201_CREATED)

        return Response({'message': 'User already exists'})

    @action(detail=False, methods=['post'])
    def verify(self, request):
        phone = request.data.get('phone')
        entered_auth_code = request.data.get('auth_code')
        try:
            profile = Profile.objects.get(phone=phone, auth_code=entered_auth_code)
            profile.auth_code = ''
            profile.invite_code = generate_invite_code()
            profile.save()
            return Response({'message': 'User verified and invite code generated'})
        except:
            return Response({'message': 'Verification failed'}, status=status.HTTP_400_BAD_REQUEST)
