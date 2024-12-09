from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db import connection
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def findServiceID(request):
    cursor = connection.cursor()
    service_id = request.POST.get('service_id')
    try:
        unique_ids = []

        cursor.execute(f"""select * from "tbl_ServiceCategory" where service_id = {service_id} """)
        
        columns = [col[0] for col in cursor.description]
        Location_list = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        unique_ids.extend(Location_list)
        return JsonResponse({'u_id':unique_ids}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def getCaseStudy(request):
    cursor = connection.cursor()
    service_name = request.POST.get('service_id')
    try:
        unique_ids = []
        cursor.execute(f"""
            select cat.category, cs."CaseStudyName", cs."Description", cs."Images" from "tbl_CaseStudy" as cs
            JOIN "tbl_ServiceCategory" as cat ON cs.service_id = cat.service_id where cat.category = '{service_name}' limit 2 """)
        
        columns = [col[0] for col in cursor.description]
        Location_list = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        unique_ids.extend(Location_list)
        return JsonResponse({'u_id':unique_ids}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def getInsights(request):
    cursor = connection.cursor()
    service_name = request.POST.get('service_id')
    try:
        unique_ids = []
        cursor.execute(f"""
            select ins."ServiceHeading", ins."Description", ins."Preview" from "tbl_Insights" as ins
            JOIN "tbl_ServiceCategory" as cat ON ins.service_id = cat.service_id where cat.category = '{service_name}' """)
        
        columns = [col[0] for col in cursor.description]
        Location_list = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        unique_ids.extend(Location_list)
        return JsonResponse({'u_id':unique_ids}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)