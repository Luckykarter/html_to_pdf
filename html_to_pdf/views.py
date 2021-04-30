from django.template import loader, Context, Template
import pdfkit
from django.http import HttpResponse
import os
from rest_framework.decorators import api_view, permission_classes
import time

TEMPLATE = 'html_to_pdf/templates/template.html'
TEST_TEMPLATE = 'html_to_pdf/templates/test_template.html'


def test_pdf(request, **kwargs):
    return make_pdf_from_html(TEST_TEMPLATE, {'test_string': 'passed!'})


@api_view(['POST'])
def make_pdf(request, **kwargs):
    files = request.FILES
    file = request.FILES.get('template')
    with open(TEMPLATE, 'wb') as f:
        if file.multiple_chunks:
            for c in file.chunks():
                f.write(c)
        else:
            f.write(file.read())
    response = make_pdf_from_html(TEMPLATE, context=request.POST)

    os.remove(TEMPLATE)
    return response


def make_pdf_from_html(template_file, context):
    with open(template_file, 'r') as f:
        template = Template(f.read())

    html = template.render(Context(context))
    filename = f'out{str(time.time())}.pdf'
    pdfkit.from_string(html, filename)
    pdf = open(filename, 'rb')
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="result.pdf"'
    pdf.close()
    os.remove(filename)

    return response
