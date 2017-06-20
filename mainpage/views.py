# Import the datetime module so that we can get the current time
import datetime

# Import the render shortcut so that we can use it to render templates
# in the response
from django.shortcuts import render

# This view method handles the request for the root URL /
# See urls.py for the mapping.
def index(request):
    # Render the index.html template with a context dictionary
    # that has a key called 'time' with current time obtained from
    # the datetime module as the value.
    return render(request, "mainpage/index.html", {'time' : datetime.datetime.now()})
