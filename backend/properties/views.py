from django.http import JsonResponse

from properties.exceptions.property import PropertyException
from properties.services.property import PropertyService

def property_view(request):
    address = request.GET.get('address')

    if not address:
        error = PropertyException(PropertyException.ErrorCode.Address_Required)
        return JsonResponse({"error": error.message}, status=error.status_code)

    data = PropertyService.get_property_by_address(address)
    if "error" in data:
       return JsonResponse(data, status=data["details"][0]["status_code"])

    return JsonResponse(data)

# Create your views here.
