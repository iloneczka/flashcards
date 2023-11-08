from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Card, Box
from .serializers import CardSerializer, BoxSerializer


class CardView(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
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
