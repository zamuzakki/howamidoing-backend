from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from leaflet.admin import LeafletGeoAdmin
from .forms import FileImportForm
from .models import Status, Report, KmGrid
from .management.commands.import_grid import check_json_loadable, check_geojson_loadable, create_grid_data

admin.site.site_header = 'How Am I Doing? Administration'

admin.site.register(Status)
admin.site.register(Report, LeafletGeoAdmin)


@admin.register(KmGrid)
class KmGridAdmin(LeafletGeoAdmin):
    change_list_template = "admin/kmgrid_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-geojson/', self.import_geojson),
        ]
        return my_urls + urls

    def import_geojson(self, request):
        if request.method == "POST":
            geojson_file = request.FILES["file"]
            content = geojson_file.read()
            is_json, json_data = check_json_loadable(content)

            if is_json:
                is_geojson, geojson_data = check_geojson_loadable(json_data)
                if is_geojson:
                    create_grid_data(geojson_data)
                else:
                    self.message_user(request, "File is not a GEOJSON file.")
            else:
                self.message_user('File is not a JSON file.')

            self.message_user(request, "Your GEOJSON file has been imported")
            return redirect("..")

        form = FileImportForm()
        payload = {"form": form}
        return render(
            request, "admin/file_import_form.html", payload
        )
