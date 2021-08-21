from django.http.response import HttpResponse
from django.shortcuts import render
from textwrap import dedent

# Create your views here.

import json
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Upload


class UploadView(CreateView):
    model = Upload
    fields = ['upload_file', ]
    success_url = reverse_lazy('fileupload')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = reversed(Upload.objects.all())
        return context

def details(request, file_id):
    doc:Upload = Upload.objects.get(pk=file_id)
    doc.status = "success"
    doc.result = dedent("""
    [
        {
            "menu": {
                "id": "file",
                "value": "File",
                "popup": {
                    "menuitem": [
                        {"value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()","value": "New", "onclick": "CreateNewDoc()","value": "New", "onclick": "CreateNewDoc()"},
                        {"value": "Open", "onclick": "OpenDoc()"},
                        {"value": "Close", "onclick": "CloseDoc()"}
                    ]
                }
            }
        },
        {
            "menu": {
                "id": "file",
                "value": "File",
                "popup": {
                    "menuitem": [
                        {"value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()","value": "New", "onclick": "CreateNewDoc()","value": "New", "onclick": "CreateNewDoc()"},
                        {"value": "Open", "onclick": "OpenDoc()"},
                        {"value": "Close", "onclick": "CloseDoc()"}
                    ]
                }
            }
        },
        {
            "menu": {
                "id": "file",
                "value": "File",
                "popup": {
                    "menuitem": [
                        {"value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()","value": "New", "onclick": "CreateNewDoc()","value": "New", "onclick": "CreateNewDoc()"},
                        {"value": "Open", "onclick": "OpenDoc()"},
                        {"value": "Close", "onclick": "CloseDoc()"}
                    ]
                }
            }
        },
        {
            "menu": {
                "id": "file",
                "value": "File",
                "popup": {
                    "menuitem": [
                        {"value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()", "value": "New", "onclick": "CreateNewDoc()","value": "New", "onclick": "CreateNewDoc()","value": "New", "onclick": "CreateNewDoc()"},
                        {"value": "Open", "onclick": "OpenDoc()"},
                        {"value": "Close", "onclick": "CloseDoc()"}
                    ]
                }
            }
        }
    ]
    """)
    return render(request, 'uploader/details.html', {'doc': doc})
    # return HttpResponse(f"file name: {doc.upload_file.name}<br><br>status: {doc.status}<br><br><p>{doc.result}</p>")

# https://docs.djangoproject.com/en/3.2/intro/tutorial03/