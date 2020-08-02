from django.contrib import admin
from .models import *

admin.site.register(base_user)
admin.site.register(manager)
admin.site.register(clerk)
#admin.site.register(hospital_manager)
admin.site.register(doctor)
admin.site.register(relation_doctor_hospital)
admin.site.register(relation_doctor_clerk)
admin.site.register(free_time)
admin.site.register(reserve)
admin.site.register(comment)



