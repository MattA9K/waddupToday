from django.contrib import admin
from coltrane.models import Category, Entry, Link



class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'slug': ['title'] }
	pass
	
	
class EntryAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'slug': ['title']}
	pass
	
	
class LinkAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'slug': ['title']}
	pass
	
	
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Link, LinkAdmin)
