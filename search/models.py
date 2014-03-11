from django.contrib import admin
from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin





class SearchKeyword(models.Model):
	keyword = models.CharField(max_length=50)
	page = models.ForeignKey(FlatPage)
	
	#kinda like a toString() method in Java
	def __unicode__(self):
		return self.keyword
		
		
		
class SearchKeywordInline(admin.StackedInline):
	model = SearchKeyword
	
	
class FlatPageAdminWithKeywords(FlatPageAdmin):
	inlines = [SearchKeywordInline]
	
	
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdminWithKeywords)


		
		

