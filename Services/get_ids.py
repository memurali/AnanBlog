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