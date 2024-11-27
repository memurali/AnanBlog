from django.shortcuts import render
import json
from django.db.models import Max, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ServiceCategory
from django.db import connection


# Create your views here.
def Add_service(request):
    return render(request, 'services/Add_service.html')

def View_service(request):
    return render(request, 'services/view_services.html')

def Service_index(request):
    return render(request, 'services/Service_index.html')

def Service_details(request):
    return render(request, 'services/Service_details.html')

@csrf_exempt
def CategoryDetails(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')

        if not category_name:
            return JsonResponse({'error': 'Category name is required'}, status=400)

        try:
            # Get the max `service_id` and calculate the next ID
            max_service_id = ServiceCategory.objects.aggregate(Max('service_id'))['service_id__max']
            new_service_id = max_service_id + 1 if max_service_id else 1

            # Check if the category already exists
            if ServiceCategory.objects.filter(category=category_name).exists():
                return JsonResponse({'error': 'Category already exists'}, status=400)
            
            # Create the new category
            ServiceCategory.objects.create(
                service_id=new_service_id,
                category=category_name
            )

            return JsonResponse({'message': 'Category created successfully'}, status=201)

        except Exception as e:
            # Log the error for debugging
            print(f"An error occurred: {e}")
            return JsonResponse({'error': 'An error occurred while creating the category'}, status=500)


    elif request.method == 'GET':
        try:
            service_id = request.GET.get('id')
            if service_id:
                categories = ServiceCategory.objects.get(service_id=service_id)
                categories_data = {
                    'service_id': categories.service_id,
                    'category': categories.category}
                return JsonResponse({'categories': categories_data})
            else:
                categories = list(ServiceCategory.objects.all().values())
                return JsonResponse({'categories': categories}, status=200)

        except Exception as e:
            # Log the error for debugging
            print(f"An error occurred while retrieving categories: {e}")
            return JsonResponse({'error': 'An error occurred while retrieving categories'}, status=500)
        

    elif request.method == 'PUT':
        try:
            # Parse the JSON data sent with the PUT request
            data = json.loads(request.body)
            category_id = data.get('id')
            new_category_name = data.get('category_name')

            print(data, category_id, new_category_name,">>>>>>>>>>>>>")

            if not category_id or not new_category_name:
                return JsonResponse({'error': 'service_id and category are required'}, status=400)

            # Retrieve the category to update
            category = ServiceCategory.objects.filter(service_id=category_id).first()

            if not category:
                return JsonResponse({'error': 'Category not found'}, status=404)

            # Update the category name
            category.category = new_category_name
            category.save()

            return JsonResponse({'message': 'Category updated successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            # Log the error for debugging
            print(f"An error occurred: {e}")
            return JsonResponse({'error': 'An error occurred while updating the category'}, status=500)
        

    elif request.method == 'DELETE':
        try:
            # Parse the JSON data sent with the DELETE request
            data = json.loads(request.body)
            category_id = data.get('id')
            category = ServiceCategory.objects.filter(service_id=category_id).first()
            category.delete()
            return JsonResponse({'message': 'Category deleted successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            # Log the error for debugging
            print(f"An error occurred: {e}")
            return JsonResponse({'error': 'An error occurred while deleting the category'}, status=500)


    # Handle invalid request methods
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def getcategory(request):
    try:
        # Initialize a cursor to execute raw SQL
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM "tbl_ServiceCategory" """)
        columns = [col[0] for col in cursor.description]
        location_list = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        cursor.close()
        return JsonResponse({'u_id': location_list}, safe=False)

    except Exception as e:
        # Log the error (Optional)
        print(f"Error: {str(e)}")

        # Return an error message in case of failure
        return JsonResponse({'error': str(e)}, status=500)
