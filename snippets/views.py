from datetime import datetime

from django.http import Http404

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):

    def get(self, request, s_num, format=None):
        snippet = self.get_code(s_num)
        if snippet.date_time is None:
            serializer = SnippetSerializer(snippet)
            response_data = serializer.data
            snippet.date_time = datetime.now()
            snippet.save()
            return Response(response_data, status=status.HTTP_200_OK)
        snippet.code = '200 EURO'
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def get_code(self, s_num):
        try:
            return Snippet.objects.get(serial_num=s_num)
        except Snippet.DoesNotExist:
            raise Http404

    def put(self, request, s_num, format=None):
        serial_object = self.get_code(s_num)
        serializer = SnippetSerializer(serial_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, code, format=None):
        serial_object = self.get_code(code)
        serial_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def code_is_valid(self, code):
        return True
