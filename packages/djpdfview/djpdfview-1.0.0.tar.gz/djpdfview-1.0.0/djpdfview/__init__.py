from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from weasyprint import HTML
import tempfile
import datetime

def pdfview(logourl, templatepath, styles, data):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=DailyTransaction' + \
        str(datetime.datetime.now())+'.pdf'
    
    response['Content-Transfer-Encoding'] = 'binary'

    context = {
        "logourl": logourl,
        "data" : data
    }

    html_string = render_to_string(templatepath, context)
    html = HTML(string=html_string)


    result = html.write_pdf(
        stylesheets=styles
    )

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response