from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.shortcuts import render, redirect
from django.urls import path
from leaflet.admin import LeafletGeoAdmin
from .forms import FileImportForm
from .models.status import Status
from .models.report import Report
from .models.km_grid import KmGrid
from .models.km_grid_score import KmGridScore
from .management.commands.import_grid import check_json_loadable, check_geojson_loadable, loop_geojson

admin.site.site_header = 'How Am I Doing? Administration'

admin.site.register(Status)
admin.site.register(Report, LeafletGeoAdmin)

class SecureOSM(gis_admin.OSMGeoAdmin):
    openlayers_url = 'https://openlayers.org/api/2.13/OpenLayers.js'
    wms_url = 'https://vmap0.tiles.osgeo.org/wms/vmap0'
    change_form_template = 'admin/change_form_template_with_admin_js.html'
    display_srid = True

@admin.register(KmGridScore)
class KmGridScoreAdmin(SecureOSM):
    list_filter = ('total_score',)

@admin.register(KmGrid)
class KmGridAdmin(SecureOSM):
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
                    loop_geojson(geojson_data)
                    self.message_user(request, "Your GEOJSON file has been imported")
                else:
                    self.message_user(request, "File is not a GEOJSON file.")
            else:
                self.message_user(request, 'File is not a JSON file.')

            return redirect("..")

        form = FileImportForm()
        payload = {"form": form}
        return render(
            request, "admin/file_import_form.html", payload
        )
