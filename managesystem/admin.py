from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Periodical)
admin.site.register(PeriodicalInfo)
admin.site.register(PeriodicalIndex)
admin.site.register(Borrow)
admin.site.register(Purchase)