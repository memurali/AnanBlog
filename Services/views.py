from django.shortcuts import render
import json
from django.db.models import Max, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db import connection
from django.core.files.storage import default_storage



# Create your views here.
@csrf_exempt
def CategoryDetails(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        Description = request.POST.get('Description')

        if not category_name:
            return JsonResponse({'error': 'Category name is required'})

        try:
            # Get the max `service_id` and calculate the next ID
            max_service_id = ServiceCategory.objects.aggregate(Max('service_id'))['service_id__max']
            new_service_id = max_service_id + 1 if max_service_id else 1

            # Check if the category already exists
            if ServiceCategory.objects.filter(category=category_name).exists():
                return JsonResponse({'message': 'Category already exists'})
            
            # Create the new category
            ServiceCategory.objects.create(
                service_id=new_service_id,
                category=category_name,
                Description = Description
            )

            return JsonResponse({'message': 'Category created successfully'})

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
                    'category': categories.category,
                    'Description': categories.Description}
                return JsonResponse({'categories': categories_data})
            else:
                categories = list(ServiceCategory.objects.all().values())
                return JsonResponse({'categories': categories})

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
            Description = data.get('Description')

            try:
                category = ServiceCategory.objects.get(service_id=category_id)  # Use ORM to fetch the instance
            except Insights.DoesNotExist:
                return JsonResponse({'error': 'Insight not found'}, status=404)
                        
            existing_insights = ServiceCategory.objects.filter(service_id=category_id, category=new_category_name, Description=Description).exists()
            if existing_insights:
                return JsonResponse({'message': 'Category Name already exists'})
        

            if not category_id or not new_category_name:
                return JsonResponse({'error': 'service_id and category are required'})

            if not category:
                return JsonResponse({'error': 'Category not found'}, status=404)

            # Update the category name
            category.category = new_category_name
            category.Description = Description
            category.save()

            return JsonResponse({'message': 'Category updated successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'})

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
            return JsonResponse({'message': 'Category deleted successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'})

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

@csrf_exempt
def findServiceDescription(request):
    try:
        # Initialize a cursor to execute raw SQL
        service_id = request.POST.get('service_id')
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * FROM "tbl_ServiceCategory" where category = '{service_id}' """)
        columns = [col[0] for col in cursor.description]
        location_list = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        cursor.close()
        return JsonResponse({'u_id': location_list}, safe=False)

    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def CaseStudyDetails(request):
    if request.method == 'POST':
        Service_name = request.POST.get('Serice_Category')
        CaseStudyName = request.POST.get('case_study')
        Description = request.POST.get('Description')
        images = request.FILES.getlist('images')

        if not CaseStudyName:
            return JsonResponse({'error': 'CaseStudy name is required'})

        # Get the max `service_id` and calculate the next ID
        max_cs_id = CaseStudy.objects.aggregate(Max('cs_id'))['cs_id__max']
        new_cs_id = max_cs_id + 1 if max_cs_id else 1

        existing_casestudy = CaseStudy.objects.filter(service=Service_name, CaseStudyName=CaseStudyName).exists()
        if existing_casestudy:
            return JsonResponse({'message': 'CaseStudy already exists for this Service'})
        
        saved_files = []
        for image in images:
            file_path = default_storage.save(f'Case_study/{image.name}', image)
            saved_files.append(file_path)

        try:
            Service = ServiceCategory.objects.get(service_id=Service_name)
        except ServiceCategory.DoesNotExist:
            return JsonResponse({'error': 'Service Category does not exist'})
                
        
        # Create the new category
        CaseStudy.objects.create(
            cs_id=new_cs_id,
            service=Service,
            CaseStudyName=CaseStudyName,
            Description = Description,
            Images = saved_files[0]
        )

        return JsonResponse({'message': 'Case Study created successfully'})


    elif request.method == 'GET':
        try:
            cs_id = request.GET.get('id')
            if cs_id:
                categories = CaseStudy.objects.get(cs_id=cs_id)
                service = categories.service  # Assuming Location_id is a ForeignKey to tbllocation
                categories_data = {
                    'cs_id': categories.cs_id,
                    'service': service,
                    'Casestudy': categories.CaseStudyName,
                    'Description': categories.Description,
                    'Image': categories.Images}
                return JsonResponse({'casestudy': categories_data})
            else:
                categories = list(CaseStudy.objects.all().values())
                return JsonResponse({'casestudy': categories})

        except Exception as e:
            # Log the error for debugging
            print(f"An error occurred while retrieving categories: {e}")
            return JsonResponse({'error': 'An error occurred while retrieving CaseStudyName'}, status=500)
        

    elif request.method == 'PUT':
        try:
            # Parse the JSON data sent with the PUT request
            data = json.loads(request.body)
            category_id = data.get('id')
            new_category_name = data.get('category_name')
            Description = data.get('Description')

            if not category_id or not new_category_name:
                return JsonResponse({'error': 'service_id and category are required'})

            # Retrieve the category to update
            category = ServiceCategory.objects.filter(service_id=category_id).first()

            if not category:
                return JsonResponse({'error': 'Category not found'}, status=404)

            # Update the category name
            category.category = new_category_name
            category.Description = Description
            category.save()

            return JsonResponse({'message': 'Category updated successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'})

        except Exception as e:
            # Log the error for debugging
            print(f"An error occurred: {e}")
            return JsonResponse({'error': 'An error occurred while updating the category'}, status=500)
        

    elif request.method == 'DELETE':
        try:
            # Parse the JSON data sent with the DELETE request
            data = json.loads(request.body)
            category_id = data.get('id')
            print(category_id,".........")
            category = ServiceCategory.objects.filter(service_id=category_id).first()
            category.delete()
            return JsonResponse({'message': 'Case Study deleted successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'})

        except Exception as e:
            # Log the error for debugging
            print(f"An error occurred: {e}")
            return JsonResponse({'error': 'An error occurred while deleting the category'}, status=500)


    # Handle invalid request methods
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def InsightsDetails(request):
    cursor = connection.cursor()
    if request.method == 'POST':
        Service_name = request.POST.get('Serice_Category')
        service_heading = request.POST.get('service_heading')
        Description = request.POST.get('Description')
        Preview =  request.POST.get('Preview')
        buy =  request.POST.get('buy')


        # Get the max `service_id` and calculate the next ID
        max_insight_id = Insights.objects.aggregate(Max('insight_id'))['insight_id__max']
        new_insight_id = max_insight_id + 1 if max_insight_id else 1

        existing_casestudy = Insights.objects.filter(service=Service_name, ServiceHeading=service_heading).exists()
        if existing_casestudy:
            return JsonResponse({'message': 'Insights already exists for this Service'})
      
        try:
            Service = ServiceCategory.objects.get(service_id=Service_name)
        except ServiceCategory.DoesNotExist:
            return JsonResponse({'error': 'Service Category does not exist'})
                
        
        # Create the new category
        Insights.objects.create(
            insight_id=new_insight_id,
            service=Service,
            ServiceHeading=service_heading,
            Description = Description,
            Preview = Preview,
            Buy = buy,
        )

        return JsonResponse({'message': 'Insights & Resources created successfully'})


    elif request.method == 'GET':
        try:
            insight_id = request.GET.get('id')            
            if insight_id:
                try:
                    insights = Insights.objects.get(insight_id=insight_id)  # Use ORM to fetch the instance
                    categories_data = {
                        'insight_id': insights.insight_id,
                        'service_id': str(insights.service_id),
                        'ServiceHeading': insights.ServiceHeading,
                        'Description': insights.Description,
                        'Preview': insights.Preview,
                        'Buy': insights.Buy,
                    }

                    return JsonResponse({'insights': categories_data})
                except Insights.DoesNotExist:
                    return JsonResponse({'error': 'Insight not found'}, status=404)
            else:
                # Return all insights if no specific ID is requested
                categories = list(Insights.objects.all().values())
                return JsonResponse({'insights': categories})
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


    elif request.method == 'PUT':
        try:
            # Parse the JSON data sent with the PUT request
            data = json.loads(request.body)
            category_id = data.get('id')
            service = data.get('Serice_Category')
            ServiceHeading = data.get('service_heading')
            Description = data.get('Description')
            Preview = data.get('Preview')
            Buy = data.get('buy')

            # Retrieve the category to update using Django's ORM
            try:
                category = Insights.objects.get(insight_id=category_id)  # Use ORM to fetch the instance
            except Insights.DoesNotExist:
                return JsonResponse({'error': 'Insight not found'}, status=404)
            
            existing_insights = Insights.objects.filter(service=service, ServiceHeading=ServiceHeading).exists()
            if existing_insights:
                return JsonResponse({'message': 'Insights already exists'})
        
            # 
            # Update the category's fields
            category.service_id = service  # Assuming service is an ID (ForeignKey)
            category.ServiceHeading = ServiceHeading
            category.Description = Description
            category.Preview = Preview
            category.Buy = Buy

            # Save the updated category
            category.save()
            return JsonResponse({'message': 'Insights updated successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'})

        except Exception as e:
            # Log the error for debugging
            print(f"An error occurred: {e}")
            return JsonResponse({'error': 'An error occurred while updating the category'}, status=500)
    

    elif request.method == 'DELETE':
        try:
            # Parse the JSON data sent with the DELETE request
            data = json.loads(request.body)
            service_id = data.get('id')
            category = Insights.objects.filter(insight_id=service_id).first()
            category.delete()
            return JsonResponse({'message': 'Insights deleted successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'})

        except Exception as e:
            # Log the error for debugging
            print(f"An error occurred: {e}")
            return JsonResponse({'error': 'An error occurred while deleting the category'}, status=500)


    # Handle invalid request methods
    return JsonResponse({'error': 'Invalid request method'}, status=405)
