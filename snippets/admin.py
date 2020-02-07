from django.contrib import admin
from django.forms import forms
from django.shortcuts import redirect, render
from django.urls import path
from snippets.models import *
from snippets.tasks import *

# Register your models here.
#
class ExcelImportForm(forms.Form):
    excel_file = forms.FileField()


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    change_list_template = "snippets/change_list.html"
    list_display = ["code", "serial_num", "value", "date_time"]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-xls/', self.import_xlsx),
        ]
        return my_urls + urls

    def import_xlsx(self, request):
        if request.method == "POST":
            ex_file = request.FILES["excel_file"]

            duplicates = ImportFromXLSX(excel_file=ex_file)
            if len(duplicates) == 0:
                self.message_user(request, "Your excel file has been imported")
            else:
                self.message_user(request, "Some codes are duplicated")
                return render(request, "snippets/duplicate_list.html", {'sheet': duplicates})
            return redirect("..")
        form = ExcelImportForm()
        payload = {"form": form}
        return render(
            request, "snippets/excel_form.html", payload
        )