import dash
import dash_core_components as dcc
import dash_html_components as html
#import pandas as pd
import collections
import plotly.graph_objs as go

from datetime import datetime as dt
from django.db.models import Count
from django_plotly_dash import DjangoDash
from django.contrib.staticfiles.templatetags.staticfiles import static


from dash.dependencies import Input, Output

from mobile.models import ServiceBooking
from users.models import UserMetadata


app = DjangoDash('MeetingRoomBookings')
app.css.append_css({'external_url': static('/css/bWLwgP.css')})

app.layout = html.Div([
    html.H4(children='Meeting Room Bookings', className='widget_header'),    
    html.Div([
            dcc.Dropdown(
                id='hotel_group',
                placeholder="Select a hotel group",
            ),      
            dcc.Dropdown(
                id='hotel',
                placeholder="Select a hotel",
            ),               
            dcc.Dropdown(
                id='city',
                placeholder="Select a city",
            ),
            dcc.DatePickerRange(
                id='date-picker-range',
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
        services = ServiceBooking.objects.filter(service__service_type='meeting_room').filter(service__hotel_group_id=hotel_group_id)\
                    .values('service__hotel_group__hotel_group_name','service__hotel_group_id')
    elif current_user.groups.filter(name='Hotel Administrators').exists(): 
        hotel_id = user_metadata.hotel_id
        services = ServiceBooking.objects.filter(service__service_type='meeting_room').filter(service__hotel_id=hotel_id)\
                    .values('service__hotel_group__hotel_group_name','service__hotel_group_id')
    else:
        services = ServiceBooking.objects.filter(service__service_type='meeting_room')\
                    .values('service__hotel_group__hotel_group_name','service__hotel_group_id') 

    
    options=[{'label': booking['service__hotel_group__hotel_group_name'], 'value': booking['service__hotel_group_id']} for booking in list(services)]

    seen = collections.OrderedDict()

    for obj in options:
        # eliminate this check if you want the last item
        if obj['value'] not in seen:
            seen[obj['value']] = obj

    return list(seen.values())

@app.expanded_callback(
    Output('hotel', 'options'),
    [Input('hotel', 'value')])
def update_drop_down(name, **kwargs):
    # get metadata for current user
    current_user = kwargs['user']
    user_id = current_user.pk
    user_metadata = UserMetadata.objects.get(user_id=user_id)

    # if group or hotel then apply filter
    if current_user.groups.filter(name='Hotel Group Administrators').exists(): 
        hotel_group_id = user_metadata.hotel_group_id
        # bookings = Booking.objects.filter(hotel_group_id=hotel_group_id)
        services = ServiceBooking.objects.filter(service__service_type='meeting_room').filter(service__hotel_group_id=hotel_group_id)\
                    .values('service__hotel__hotel_name', 'service__hotel_id')
    elif current_user.groups.filter(name='Hotel Administrators').exists(): 
        hotel_id = user_metadata.hotel_id
        services = ServiceBooking.objects.filter(service__service_type='meeting_room').filter(service__hotel_id=hotel_id)\
                    .values('service__hotel__hotel_name', 'service__hotel_id')
    else:
        services = ServiceBooking.objects.filter(service__service_type='meeting_room')\
                    .values('service__hotel__hotel_name','service__hotel_id')        
    
    options=[{'label': booking['service__hotel__hotel_name'], 'value': booking['service__hotel_id']} for booking in list(services)]

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
        services = ServiceBooking.objects.filter(service__service_type='meeting_room').filter(service__hotel_group_id=hotel_group_id)\
                    .values('service__hotel__city')
    elif current_user.groups.filter(name='Hotel Administrators').exists(): 
        hotel_id = user_metadata.hotel_id
        services = ServiceBooking.objects.filter(service__service_type='meeting_room').filter(service__hotel_id=hotel_id)\
                    .values('service__hotel__city')
    else:
        services = ServiceBooking.objects.filter(service__service_type='meeting_room')\
                    .values('service__hotel__city')        
    
    options=[{'label': booking['service__hotel__city'], 'value': booking['service__hotel__city']} for booking in list(services)]

    seen = collections.OrderedDict()

    for obj in options:
        # eliminate this check if you want the last item
        if obj['value'] not in seen:
            seen[obj['value']] = obj

    return list(seen.values())       

@app.expanded_callback(
    Output("bookings-graph", "figure"),
    [Input("hotel_group", "value"),
    Input("hotel", "value"),
    Input("city", "value"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date")]
)
def update_graph(hotel_group_id, hotel_id, hotel__city, start_date, end_date, **kwargs):
    
    # get metadata for current user
    current_user = kwargs['user']
    user_id = current_user.pk
    user_metadata = UserMetadata.objects.get(user_id=user_id)

    hotel_group_filter = {} if hotel_group_id == None else {"service__hotel_group_id": hotel_group_id}
    hotel_filter = {} if hotel_id == None else {"service__hotel_id": hotel_id}
    hotel__city_filter = {} if hotel__city == None else {"service__hotel__city": hotel__city}
    servicebooking_start_date_filter = {} if start_date == None else {"start_date_time__gte": dt.strptime(start_date.split(' ')[0], '%Y-%m-%d')}
    servicebooking_end_date_filter = {} if end_date == None else {"end_date_time__lte": dt.strptime(end_date.split(' ')[0], '%Y-%m-%d')}

    # if group or hotel then apply filter
    if current_user.groups.filter(name='Hotel Group Administrators').exists(): 
        hotel_group_id = user_metadata.hotel_group_id
        # bookings = Booking.objects.filter(hotel_group_id=hotel_group_id)
        services = ServiceBooking.objects.filter(service__service_type='meeting_room').filter(hotel_group_id=hotel_group_id)\
                    .filter(**hotel__city_filter).filter(**hotel_filter).filter(**servicebooking_start_date_filter)\
                    .filter(**servicebooking_end_date_filter)\
                    .values('service__hotel_id', 'service__hotel__hotel_name')\
                    .annotate(total=Count('service__hotel_id'))
    elif current_user.groups.filter(name='Hotel Administrators').exists(): 
        hotel_id = user_metadata.hotel_id
        services = ServiceBooking.objects.filter(service__service_type='meeting_room').filter(hotel_id=hotel_id)\
                    .filter(**servicebooking_start_date_filter).filter(**servicebooking_end_date_filter)\
                    .values('service__hotel_id', 'service__hotel__hotel_name')\
                    .annotate(total=Count('service__hotel_id'))
    else:
        services = ServiceBooking.objects.filter(**hotel_group_filter).filter(service__service_type='meeting_room')\
                    .filter(**hotel__city_filter).filter(**hotel_filter).filter(**servicebooking_start_date_filter)\
                    .filter(**servicebooking_end_date_filter)\
                    .values('service__hotel_id', 'service__hotel__hotel_name')\
                    .annotate(total=Count('service__hotel_id'))             

    if len(services) == 0:
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
        values=[booking['total'] for booking in list(services)]
        labels=[booking['service__hotel__hotel_name'] for booking in list(services)]

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