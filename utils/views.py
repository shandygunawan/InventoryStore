import json
import os
import pathlib
import datetime

from os import listdir
from os.path import isfile, join
from io import StringIO

from django.http import JsonResponse
from django.core.management import call_command
from django.conf import settings
from django.views.static import serve

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

"""
============================
SERVER HEALTH
============================
"""
def checkHealth(request):
    response = {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": None
    }

    return JsonResponse(response, status=status.HTTP_200_OK)


"""
============================
BACKUP DB
============================
"""
class listBackupLocal(APIView):
    permission_classes = (IsAuthenticated, )

    # Get list Backup + Backup Info
    def get(self, request):
        backup_path = settings.DBBACKUP_STORAGE_OPTIONS['location']
        backup_files = [f for f in listdir(backup_path) if isfile(join(backup_path, f))]

        response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": None,
            "data": backup_files
        }
        return Response(response, status.HTTP_200_OK)

    # Download specific version of db
    def post(self, request):
        backup_path = settings.DBBACKUP_STORAGE_OPTIONS['location']
        backup_files = [f for f in listdir(backup_path) if isfile(join(backup_path, f))]

        req = json.loads(request.body)
        if req['backup_name'] in backup_files:
            filepath = backup_path + "/" + req['backup_name']
            return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
        else:
            response = {
                "success": False,
                "message": "File not exist!",
                "status_code": status.HTTP_400_BAD_REQUEST
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def listBackupDropbox(request):
    backup_files_raw = StringIO()
    call_command("listbackups", stdout=backup_files_raw)
    
    backup_files_raw = backup_files_raw.getvalue().split("\n")
    backup_files = []
    for i in range(1, len(backup_files_raw)-1):
        backup_file = backup_files_raw[i].split(" ")

        datetime_raw = backup_file[1] + " " + backup_file[2]
        datetime_object = datetime.datetime.strptime(datetime_raw, "%m/%d/%y %H:%M:%S")

        backup_files.append({
            "name": backup_file[0],
            "datetime": datetime_object.isoformat()
        })

    response = {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": None,
        "data": backup_files
    }

    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def backupDb(request):
    try:
        call_command("dbbackup")
        response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": None
        }
        return Response(response, status.HTTP_200_OK)
    except Exception as e:
        response = {
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }
        return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def backupInfo(request):
    # backup_path = settings.DBBACKUP_STORAGE_OPTIONS['location']
    # backup_files = [f for f in listdir(backup_path) if isfile(join(backup_path, f))]

    # created_times = []

    # for backup_file in backup_files:
    #     fname = pathlib.Path(backup_path + backup_file)
    #     created_times.append(datetime.datetime.fromtimestamp(fname.stat().st_ctime))

    # created_times = sorted(created_times, reverse=True)

    response = {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": None,
        "data": {
            # "time_createdbackup_latest_server": created_times[0],
            "time_autobackup": settings.AUTOBACKUP_TIME,
            "location_backup": settings.AUTOBACKUP_LOCATION
        }
    }
    return Response(response, status.HTTP_200_OK)