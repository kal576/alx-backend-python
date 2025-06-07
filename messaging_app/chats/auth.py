from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Handle user registration.
        Expects 'username', 'email', 'password', and optional fields.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                {'message': 'User created successfully', 'user_id': user.user_id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating user profile.
    Only authenticated users can access their own profile.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Override to return the current user's profile.
        """
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)
    
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle user login.
        Expects 'username' and 'password'.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)