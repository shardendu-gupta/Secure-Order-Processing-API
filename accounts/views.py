from rest_framework import generics, status
from .serializers import RegistrationSerializer
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):

    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({"msg": "User registered succefully.", "user": {"id": user.id, "username": user.username, "email": user.email}},
                         status=status.HTTP_201_CREATED)






