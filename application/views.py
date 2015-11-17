# -*- coding: utf-8 -*-

"""
views.py
URL route handlers
"""
import traceback

import json

from datetime import datetime

#from google.appengine.api import users
#from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, jsonify, render_template, abort, send_from_directory

#from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from models import EventModel, TicketModel
from cities import cities_dict

# Flask-Cache (configured to use App Engine Memcache API)
# cache = Cache(app)


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/events', methods=['GET'])
def list_events_json():
    """List all events in json format"""
    events = EventModel.objects()
    events = [event.serialize for event in events]
    return jsonify(data=events)

@app.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):    
    event = EventModel.objects.get(id=event_id)    
    if not event:
        return abort(404)
    return jsonify(data=event.serialize)

@app.route('/events/<int:event_id>/update', methods=['POST'])
def update_event(event_id):
    try:        
        event = EventModel.objects.get(_id=event_id)
        if not event:
            return abort(404)
        posted_event = request.get_json()        
        event.event_name = posted_event['event_name']
        event.event_description = posted_event['event_description']
        event.event_date = datetime.strptime(posted_event['event_date'][:10], '%Y-%m-%d')
        event.event_state = posted_event['event_state']
        event.event_city = posted_event['event_city']
        event.event_img = posted_event['event_img']
        event.save()
        return jsonify(status='success')
    except:
        return jsonify(status='error', msg='Unknown error.')

@app.route('/events/insert', methods=['POST'])
def insert_event():
    try:
        event = EventModel()
        posted_event = request.get_json()        
        event.event_name = posted_event['event_name']
        event.event_description = posted_event['event_description']
        event.event_date = datetime.strptime(posted_event['event_date'][:10], '%Y-%m-%d')
        event.event_state = posted_event['event_state']
        event.event_city = posted_event['event_city']
        event.event_img = posted_event['event_img']
        event.save()
        return jsonify(status='success')
    except Exception as e:
        traceback.print_exc()
        return jsonify(status='error', msg='Unknown error.' )

@app.route('/events/<int:event_id>/tickets/new', methods=['POST'])
def add_ticket(event_id):
    event = EventModel.get_by_id(event_id)
    if not event:
        return abort(404)
    posted_ticket = request.get_json()        
    ticket = TicketModel()
    ticket.ticket_seller_mail = posted_ticket['ticket_seller_mail']
    ticket.ticket_price = posted_ticket['ticket_price']
    ticket.ticket_type = posted_ticket['ticket_type']
    ticket.ticket_amount = posted_ticket['ticket_amount']
    try:
        event.tickets.append(ticket)
        event.save()
        return jsonify(status='success')
    except:
        return jsonify(status='error', msg='Unknown error.')

@app.route('/events/<int:event_id>/tickets', methods=['GET'])
def event_tickets(event_id):
    event = EventModel.get_by_id(event_id)
    if not event:
        return abort(404)
    tickets = event.tickets
    tickets = [ticket.serialize for ticket in tickets]
    return jsonify(data=tickets)

@app.route('/events/<int:event_id>/delete', methods=['POST',])
def delete_event(event_id):
    """Delete an event object"""
    event = EventModel.get_by_id(event_id)
    try:
        event.key.delete()
        return jsonify(data='success')
    except:
        return jsonify(status='error', msg='Unknown error.')


@app.route('/states/<state>/cities', methods=['GET',])
def get_state_cities(state):
    for estado in cities_dict['estados']:
        if estado['sigla'] == state:
            return jsonify(data=estado['cidades'])
    return abort(404)


#def logout():
#    """This view requires an admin account"""
#    return redirect((users.create_logout_url('/'))) 


