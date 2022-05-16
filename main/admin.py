from django.contrib import admin
from .models import packet,Document, MainPCAP


admin.site.register(packet)
admin.site.register(Document)
admin.site.register(MainPCAP)
# Register your models here.
