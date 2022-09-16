import base64
from io import BytesIO
from django.conf import settings
from math import radians, cos, sin, asin, sqrt

from django.core.files.base import ContentFile
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import HttpResponse
from django.contrib.auth.models import Permission
from django.core.mail import send_mail
import datetime


BaseUrl = 'http://192.168.43.60:8000/'

# ☺ Python 3 program to calculate Distance Between Two Points on Earth
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
    '''
    lat1 = 4.05 # Douala latitude
    lat2 = 3.866667 # Yaoundé latitude
    lon1 = 9.7 # Douala longitude
    lon2 = 11.516667 # Yaoundé longitude
    print(distance(lat1, lat2, lon1, lon2), "K.M")
    '''
      
    # calculate the result
    return(c * r)


def generateReport(params: dict):
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


def baseUrl():
    return BaseUrl


def save_pdf(params: dict, doc_name=None):
    template = get_template("users.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    date = datetime.datetime.now()
    if doc_name:
        filename = "{0}-{1}.pdf".format(
            str("{0}-{1}-{2}-{3}-{4}-{5}".format(date.year, date.month, date.day, date.hour, date.minute, date.second)),
            doc_name)
    else:
        filename = "{0}.pdf".format(date.timestamp())

    try:
        with open(str(settings.BASE_DIR) + f'/media/pdfs/{filename}', "wb+") as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)
    except Exception as e:
        print(e)

    if pdf.err:
        return '', False

    return filename, True


def send_email():
    send_mail("Salutation", "Bonjour M/Mme. Comment allez-vous ?", 'larissasignie@gmail.com', \
              ['patrickkennenl@gmail.com'], fail_silently=False)


def hasPermission(request=None, codename=None):
    '''
        has_perm = hasPermission(request, 'pharmashop.add_carnet')
    '''
    if not request.user.id:
        return None
    return request.user.has_perm(codename)


def addPermission(request=None, codename=None):
    '''
        add_perm = addPermission(request, 'add_carnet')
    '''
    if not request.user.id:
        return None
    perm = Permission.objects.get(codename=codename)
    request.user.user_permissions.add(perm)
    request.user.save()
    return True


def removePermission(request=None, codename=None):
    '''
        remove_perm = removePermission(request, 'add_carnet')
    '''
    if not request.user.id:
        return None
    perm = Permission.objects.get(codename=codename)
    request.user.user_permissions.remove(perm)
    request.user.save()
    return True


def clearPermissions(request=None):
    '''
        clear_perms = clearPermission(request)
    '''
    if not request.user.id:
        return None
    request.user.user_permissions.clear()
    request.user.save()
    return True


def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))
