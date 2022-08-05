
from math import radians, cos, sin, asin, sqrt

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import HttpResponse



#☺ Python 3 program to calculate Distance Between Two Points on Earth

def distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # driver code
    lat1 =  4.05 # Douala latitude
    lat2 =  3.866667 # Yaoundé latitude
    lon1 = 9.7 # Douala longitude
    lon2 = 11.516667 # Yaoundé longitude
    print(distance(lat1, lat2, lon1, lon2), "K.M")
      
    # calculate the result
    return(c * r)


def generateReport(params:dict):
    users = params
    template_path = "users.html"
    response = HttpResponse(content_type="application/pdf")
    # response['Content-Disposition'] = 'attachment; filename="users_report.pdf"'
    response['Content-Disposition'] = 'filename="Liste des utilisateurs.pdf"'
    template = get_template(template_path)

    html = template.render(params)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return
    return response 
     
