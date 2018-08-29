from django.shortcuts import render_to_response
from django.template import RequestContext

def app(request):
	return render_to_response('app.html')
