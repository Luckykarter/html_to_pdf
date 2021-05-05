from django.template import loader, Context, Template
import pdfkit
from django.http import HttpResponse
import os
from rest_framework.decorators import api_view, permission_classes
import time

TEMPLATE = 'html_to_pdf/templates/template.html'
FOLDER = 'html_to_pdf/templates/'
TEST_TEMPLATE = 'html_to_pdf/templates/test_template.html'


def test_pdf(request, **kwargs):
    return make_pdf_from_html(TEST_TEMPLATE, {'test_string': 'passed!'})


@api_view(['POST'])
def make_pdf(request, **kwargs):
    template_filename = ''
    context = request.POST.copy()
    folder = os.path.join(FOLDER, str(time.time()).replace('.', ''))
    context['image_path'] = os.path.abspath(folder)
    os.mkdir(folder)
    filenames = set()
    for file_tag in request.FILES:
        file = request.FILES.get(file_tag)
        filename = os.path.join(folder, file.name)
        if file_tag == 'template':
            template_filename = filename

        filenames.add(filename)
        with open(filename, 'wb') as f:
            if file.multiple_chunks:
                for c in file.chunks():
                    f.write(c)
            else:
                f.write(file.read())

    response = make_pdf_from_html(template_filename, context=context)
    for filename in filenames:
        os.remove(filename)
    os.rmdir(folder)
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
