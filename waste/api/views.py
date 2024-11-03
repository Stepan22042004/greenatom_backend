from djoser.views import UserViewSet
from organisations.models import Organisation, Storage, User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from api.serializers import (OrganisationSerializer, StorageSerializer,
                             DistanceSerializer, GenerateSerializer,
                             UtilizeSerializer, UserSerializer,
                             PutOrganisationSerializer)
from api.permissions import IsEmployeeOrAdmin


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=['put', 'delete'],
        permission_classes=(IsAdminUser,),
        detail=True,
        url_path='add_organisation'
    )
    def add_organisation(self, request, id=None):
        user = User.objects.get(id=id)
        if request.method == 'PUT':
            serializer = PutOrganisationSerializer(
                user,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = request.user
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = (IsEmployeeOrAdmin,)

    @action(methods=['patch'], detail=True, url_path='change_distance')
    def change_distance(self, request, pk=None):
        organisation = Organisation.objects.get(pk=pk)
        serializer = DistanceSerializer(
                organisation,
                data=request.data,
                context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True, url_path='generate_waste')
    def generate_waste(self, request, pk=None):
        organisation = Organisation.objects.get(pk=pk)
        serializer = GenerateSerializer(
                organisation,
                data=request.data,
                context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='utilize')
    def utilize(self, request, pk=None):
        organisation = Organisation.objects.get(pk=pk)
        serializer = UtilizeSerializer(
                organisation,
                data=request.data,
                context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = (IsAdminUser,)
