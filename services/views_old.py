from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from services.models import Building
from services.serializers import BuildingSerializer


@api_view(['GET', 'POST'])
def Building_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Building.objects.all()
        serializer = BuildingSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BuildingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def Building_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code Building.
    """
    try:
        targetBuilding = Building.objects.get(pk=pk)
    except Building.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BuildingSerializer(targetBuilding)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BuildingSerializer(targetBuilding, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        targetBuilding.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)