from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Status, Report, KmGrid

admin.site.site_header = 'How Am I Doing? Administration'

admin.site.register(Status)
admin.site.register(Report, LeafletGeoAdmin)
admin.site.register(KmGrid, LeafletGeoAdmin)
