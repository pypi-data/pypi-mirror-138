#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2021/12/21 15:30
    Desc  :
--------------------------------------
"""
from .common.request import BaseAPIView
from .common.response import SuccessResponse, SystemExceptionResponse
from .models import Log
from .serializers import RequestLogSerializer


class LogsBaseView(BaseAPIView):
    Model = Log

    search_fields = ["path", "method", "operatorName"]

    queryset = Log.objects.all()

    serializer_class = RequestLogSerializer


class LogsListView(LogsBaseView):

    def post(self, request, *args, **kwargs):
        """
        获取日志列表
        """
        try:
            data = request.data.copy()
            page, size = data.get('page'), data.get('size')
            if len(self.search_fields) != 0:
                queryset = self.Model.objects.filter(**self.search_queryset(request))
            else:
                queryset = self.Model.objects.all()

            serializer = self.get_serializer(queryset, many = True)
            pageData = Paginator(serializer.data, size)
            data = {
                'totalSize': pageData.count,
                'page': page,
                'size': size,
                'array': pageData.page(page).object_list
            }
            return SuccessResponse(result = data)

        except Exception:
            return SystemExceptionResponse()


class LogsInfoView(LogsBaseView):

    def post(self, request, *args, **kwargs):
        """
        获取日志列表
        """
        try:
            data = request.data.copy()
            logId = ObjectId(data.get('logId'))
            queryset = self.Model.objects.filter(id = logId)
            serializer = self.get_serializer(queryset.first())
            return SuccessResponse(result = serializer.data)

        except Exception as e:
            return SystemExceptionResponse()


urlpatterns = [
    path('list', LogsListView.as_view()),
    path('info', LogsInfoView.as_view()),
]
