import json
import os
import pathlib
import glob
import datetime
import sys

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

import dropbox

from igog.models import Incoming, Outgoing
from products.models import Product
from entities.models import Supplier, Buyer
from utils.models import GlobalConfig

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
GLOBAL CONFIG
============================
"""

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def setGlobalConfig(request):
    req = json.loads(request.body)

    changed_keys = []
    for key in req.keys():
        try:
            config = GlobalConfig.objects.get(key=key)
        except GlobalConfig.DoesNotExist:
            config = None

        if config:
            config.value = req[key]
            config.save()
            changed_keys.append(key)

    response = {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": None,
        "data": changed_keys
    }
    return Response(response, status=status.HTTP_200_OK)


"""
============================
DB INFO
============================
"""
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def dbInfo(request):
    try:
        # Getting object count
        count_incoming = Incoming.objects.count()
        count_outgoing = Outgoing.objects.count()
        count_product = Product.objects.count()
        count_supplier = Supplier.objects.count()
        count_buyer = Buyer.objects.count()

        # Get size per table
        size_incoming = sys.getsizeof(Incoming()) * count_incoming
        size_outgoing = sys.getsizeof(Incoming()) * count_outgoing
        size_product = sys.getsizeof(Incoming()) * count_product
        size_supplier = sys.getsizeof(Incoming()) * count_supplier
        size_buyer = sys.getsizeof(Incoming()) * count_buyer

        response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": None,
            "data": {
                "count": {
                    "incoming": count_incoming,
                    "outgoing": count_outgoing,
                    "product": count_product,
                    "supplier": count_supplier,
                    "buyer": count_buyer
                },
                "size": {
                    "incoming": size_incoming,
                    "outgoing": size_outgoing,
                    "product": size_product,
                    "supplier": size_supplier,
                    "buyer": size_buyer
                }
            }
        }

        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        response = {
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
============================
BACKUP DB
============================
"""


class listBackupLocal(APIView):
    permission_classes = (IsAuthenticated,)

    # Get list Backup + Backup Info
    def get(self, request):
        backup_path = settings.DBBACKUP_STORAGE_OPTIONS['location']
        backup_filenames = [f for f in listdir(backup_path) if isfile(join(backup_path, f))]

        backup_files = []
        for backup_filename in backup_filenames:
            fname = pathlib.Path(backup_path + backup_filename)
            created_time = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
            backup_files.append({
                "name": backup_filename,
                "datetime": created_time
            })

        backup_files = sorted(backup_files, key=lambda k: k['datetime'], reverse=True)

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
                "message": "File not exist",
                "status_code": status.HTTP_400_BAD_REQUEST
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def backupDb(request):
    try:
        # Use dbbackup to local
        call_command("dbbackup")

        # Upload to Cloud (Dropbox)
        list_of_backups = glob.glob(settings.DBBACKUP_STORAGE_OPTIONS['location'] + "*.dump")
        latest_backup = max(list_of_backups, key=os.path.getctime) # Get latest backup for upload

        backup_filename = latest_backup.split("\\")[-1]
        dbx = dropbox.Dropbox(open("keys/access_dropbox.txt", "r").read()) # Instantiate dropbox
        with open(latest_backup, 'rb') as f:
            dbx.files_upload(f.read(), GlobalConfig.objects.get(key="autobackup_location").value + backup_filename)

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
@permission_classes((IsAuthenticated,))
def backupInfo(request):
    autobackup_time = GlobalConfig.objects.get(key="autobackup_time").value
    autobackup_location = GlobalConfig.objects.get(key="autobackup_location").value

    response = {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": None,
        "data": {
            "autobackup_time": autobackup_time,
            "autobackup_location": autobackup_location
        }
    }
    return Response(response, status.HTTP_200_OK)
