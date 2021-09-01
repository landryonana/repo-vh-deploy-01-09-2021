from django.contrib import admin

from remplissages.models import Evangelisation,  Person, Site, Suivie, Image, Participant


admin.site.register(Evangelisation)
admin.site.register(Person)
admin.site.register(Site)
admin.site.register(Image)
admin.site.register(Suivie)
admin.site.register(Participant)
