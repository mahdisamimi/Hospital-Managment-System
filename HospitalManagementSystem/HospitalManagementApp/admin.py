from django.contrib import admin
from .models import *

admin.site.register(user)
admin.site.register(hospital)
admin.site.register(clerk)
#admin.site.register(hospital_manager)
admin.site.register(doctor)
admin.site.register(relation_doctor_hospital)
admin.site.register(relation_doctor_clerk)
admin.site.register(free_time)
admin.site.register(reserve)
admin.site.register(comment)



