from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Card, Box
from .serializers import CardSerializer, BoxSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.views import LoginView
from rest_framework.authtoken.models import Token


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Twój plik szablonu z formularzem logowania

    def form_valid(self, form):
        response = super().form_valid(form)
        # Generuj token po pomyślnym zalogowaniu
        token, created = Token.objects.get_or_create(user=self.user)
        return response


class YourApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Twój kod dla widoku YourApiView
        return Response({'message': 'Hello from YourApiView!'})


class CardView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Card.objects.none()
        return Card.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['user'] = self.request.user

        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'cards': serializer.data, 'user': request.user.id})


class BoxView(viewsets.ModelViewSet):
    serializer_class = BoxSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Box.objects.none()
        return Box.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        box_number = request.data.get('box_number')

        if Box.objects.filter(user=user, box_number=box_number).exists():
            return Response({'detail': 'Box with this number already exists for the current user.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'boxes': serializer.data, 'user': request.user.id})
