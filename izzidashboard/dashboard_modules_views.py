from django.conf.urls import url
from django.contrib import messages
from django.shortcuts import redirect, render
from jet.dashboard import dashboard
import pandas as pd

def index(request):
    """ view function for sales app """

    # read data 
    table_content = "this is table context"                                                                                             
	
    context = {'table_data': table_content}
    return render(request, 'cms/dashboard_modules/test.html', context=context)

# This method registers view's url
dashboard.urls.register_urls([
    url(
        r'^test/',
        index,
        name='test'
    ),
])