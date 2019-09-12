from django.contrib import admin
from .models import Tailwind, TailwindOrder, TailwindUserConfig

admin.site.register(Tailwind)
admin.site.register(TailwindOrder)
admin.site.register(TailwindUserConfig)

