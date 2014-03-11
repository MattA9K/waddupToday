from django.shortcuts import render, render_to_response

from django.http import HttpResponse
from django.template import loader, Context
from django.contrib.flatpages.models import FlatPage
# Create your views here.


#def search(request):
#	query = request.GET['q']
#	results = FlatPage.objects.filter(content__icontains=query)
#	template = loader.get_template('search.html')
#	context = Context({ 'query':query, 'results': results })
#	response = template.render(context)
#	return HttpResponse(response)



# ALTERNATE WAY TO HANDLE THE SEARCH FUNCTION :

def search(request):
	query = request.GET['q']
	return render_to_response('search.html',
								{ 'query':query,
								'results': FlatPage.objects.filter(
										content__icontains=query) })