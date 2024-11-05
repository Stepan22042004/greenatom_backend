from django.contrib import admin

from organisations.models import (User, Capacity, Storage,
			  Organisation, StorageCapacity,
			  OrganisationCapacity, OrganisationStorage)

admin.site.register(User)
admin.site.register(Capacity)
admin.site.register(Storage)
admin.site.register(Organisation)
admin.site.register(StorageCapacity)
admin.site.register(OrganisationCapacity)
admin.site.register(OrganisationStorage)
