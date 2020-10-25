import dash
import dash_core_components as dcc
import dash_html_components as html
#import pandas as pd
import collections
import plotly.graph_objs as go
import numpy as np

from django.db.models import Count
from django_plotly_dash import DjangoDash
from django.contrib.staticfiles.templatetags.staticfiles import static

from dash.dependencies import Input, Output

from cms.models import Booking
from users.models import UserMetadata


app = DjangoDash('ConfirmedBookings')
app.css.append_css({'external_url': static('/css/bWLwgP.css')})

app.layout = html.Div([
    html.H4(children='Confirmed Bookings', style={
        'font-family': '"Roboto", "Helvetica", "Arial", "sans-serif"',
        'color': '#3C4858',
        'margin-top': '15px',
        'min-height': 'auto',
        'font-weight': '300',
        'margin-bottom': '0px',
        'text-decoration': 'none',   
        'font-size': '1.3em',
        'line-height': '1.4em', 
        'margin-bottom': '5px' 
    }),
    html.Div([
            dcc.Dropdown(
                id='hotel_group',
                placeholder="Select a hotel group",
            ),       
            dcc.Dropdown(
                id='city',
                placeholder="Select a city",
            ),
        ],
    ),
    dcc.Graph(id='bookings-graph'),    
])

@app.expanded_callback(
    Output('hotel_group', 'options'),
    [Input('hotel_group', 'value')])
def update_drop_down(name, **kwargs):
    # get metadata for current user
    current_user = kwargs['user']
    user_id = current_user.pk
    user_metadata = UserMetadata.objects.get(user_id=user_id)

    # if group or hotel then apply filter
    if current_user.groups.filter(name='Hotel Group Administrators').exists(): 
        hotel_group_id = user_metadata.hotel_group_id
        # bookings = Booking.objects.filter(hotel_group_id=hotel_group_id)
        bookings = Booking.objects.filter(hotel_group_id=hotel_group_id).filter(booking_status=1)\
                    .values('hotel_id, hotel_hotel_name, hotel_group_hotel_group_name, hotel_group_id, city_city_name')\
                    .annotate(total=Count('hotel_id'))
    elif current_user.groups.filter(name='Hotel Administrators').exists(): 
        hotel_id = user_metadata.hotel_id
        bookings = Booking.objects.filter(hotel_id=hotel_id).filter(booking_status=1)\
                    .values('hotel_id, hotel_hotel_name, hotel_group_hotel_group_name, hotel_group_id, city_city_name')\
                    .annotate(total=Count('hotel_id'))
    else:
        bookings = Booking.objects.all().filter(booking_status=1)\
                    .values('hotel_id', 'hotel__hotel_name', 'hotel_group__hotel_group_name', 'hotel_group_id', 'hotel__city')\
                    .annotate(total=Count('hotel_id'))         

    
    options=[{'label': booking['hotel_group__hotel_group_name'], 'value': booking['hotel_group_id']} for booking in list(bookings)]

    seen = collections.OrderedDict()

    for obj in options:
        # eliminate this check if you want the last item
        if obj['value'] not in seen:
            seen[obj['value']] = obj

    return list(seen.values())

@app.expanded_callback(
    Output('city', 'options'),
    [Input('city', 'value')])
def update_drop_down(name, **kwargs):
    # get metadata for current user
    current_user = kwargs['user']
    user_id = current_user.pk
    user_metadata = UserMetadata.objects.get(user_id=user_id)

    # if group or hotel then apply filter
    if current_user.groups.filter(name='Hotel Group Administrators').exists(): 
        hotel_group_id = user_metadata.hotel_group_id
        # bookings = Booking.objects.filter(hotel_group_id=hotel_group_id)
        bookings = Booking.objects.filter(hotel_group_id=hotel_group_id).filter(booking_status=1)\
                    .values('hotel_id, hotel_hotel_name, hotel_group_hotel_group_name, hotel_group_id, city_city_name')\
                    .annotate(total=Count('hotel_id'))
    elif current_user.groups.filter(name='Hotel Administrators').exists(): 
        hotel_id = user_metadata.hotel_id
        bookings = Booking.objects.filter(hotel_id=hotel_id).filter(booking_status=1)\
                    .values('hotel_id, hotel_hotel_name, hotel_group_hotel_group_name, hotel_group_id, city_city_name')\
                    .annotate(total=Count('hotel_id'))
    else:
        bookings = Booking.objects.all().filter(booking_status=1)\
                    .values('hotel_id', 'hotel__hotel_name', 'hotel_group__hotel_group_name', 'hotel_group_id', 'hotel__city')\
                    .annotate(total=Count('hotel_id'))        

    options=[{'label': booking['hotel__city'], 'value': booking['hotel__city']} for booking in list(bookings)]

    seen = collections.OrderedDict()

    for obj in options:
        # eliminate this check if you want the last item
        if obj['value'] not in seen:
            seen[obj['value']] = obj

    return list(seen.values())       

@app.expanded_callback(
    Output("bookings-graph", "figure"),
    [Input("hotel_group", "value"),
    Input("city", "value")]
)
def update_graph(hotel_group_id, hotel__city, **kwargs):
    # get metadata for current user
    current_user = kwargs['user']
    user_id = current_user.pk
    user_metadata = UserMetadata.objects.get(user_id=user_id)

    hotel_group_filter = {} if hotel_group_id == None else {"hotel_group_id": hotel_group_id}
    hotel__city_filter = {} if hotel__city == None else {"hotel__city": hotel__city}

    # if group or hotel then apply filter
    if current_user.groups.filter(name='Hotel Group Administrators').exists(): 
        hotel_group_id = user_metadata.hotel_group_id
        # bookings = Booking.objects.filter(hotel_group_id=hotel_group_id)
        bookings = Booking.objects.filter(hotel_group_id=hotel_group_id).filter(**hotel__city_filter).filter(booking_status=1)\
                    .values('hotel_id, hotel_hotel_name, hotel_group_hotel_group_name, hotel_group_id, city_city_name') \
                    .annotate(total=Count('hotel_id'))
    elif current_user.groups.filter(name='Hotel Administrators').exists(): 
        hotel_id = user_metadata.hotel_id
        bookings = Booking.objects.filter(hotel_id=hotel_id).filter(booking_status=1)\
                    .values('hotel_id, hotel_hotel_name, hotel_group_hotel_group_name, hotel_group_id, city_city_name') \
                    .annotate(total=Count('hotel_id'))
    else:
        bookings = Booking.objects.filter(**hotel_group_filter).filter(**hotel__city_filter).filter(booking_status=1)\
                    .values('hotel_id', 'hotel__hotel_name', 'hotel_group__hotel_group_name', 'hotel_group_id', 'hotel__city') \
                    .annotate(total=Count('hotel_id'))             

    if len(bookings) == 0:
        return {
            "data": [go.Pie(labels=[], values=[], textinfo='label')],
            "layout": go.Layout({
                "annotations": [
                    {
                        "text": "No matching data found",
                        "showarrow": False
                    }
                ]
            })
        }         
    else: 
        values=[booking['total'] for booking in list(bookings)]
        labels=[booking['hotel__hotel_name'] for booking in list(bookings)]

        return {
            "data": [go.Pie(labels=labels, values=values, textinfo='none')],
            "layout": go.Layout(
                margin=dict(
                    l=50,
                    r=50,
                    b=0,
                    t=50,
                    pad=0
                ),  
                autosize=True,      
                width=350,
                legend=dict(
                    y=1.1,
                    orientation='h',
                ),  
                colorway=['#2e3164','#e5e7fe','#c3c7ca']
            )
        }             