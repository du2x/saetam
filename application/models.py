"""
models.py
Mongoengine models
"""

from mongoengine import *    
from cities import cities_dict

import datetime

connect('saeta')

cities_states = [estado['cidades'] for estado in cities_dict['estados']]
cities = sum(cities_states, [])

states = [estado['sigla'] for estado in cities_dict['estados']]


class UserModel(EmbeddedDocument):
    """ User Model """
    user_name = StringField()
    user_phonenumber = StringField()
    user_email = StringField()


class TicketModel(EmbeddedDocument):
    """ Ticket Announcement Model """
    ticket_seller_mail = StringField(required=True)
    ticket_price = StringField(required=True)
    ticket_type = StringField()
    ticket_amount = IntField(required=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = EmbeddedDocumentField('UserModel')

    @property
    def serialize(self):        
        return {
            'seller': self.ticket_seller_mail,
            'price': self.ticket_price,
            'type': self.ticket_type
        }


class EventModel(Document):
    """Event Model"""
    event_name = StringField(required=True)
    event_description = StringField()
    event_date = DateTimeField()
    event_img = StringField(required=True)
    event_state = StringField(choices=states)
    event_city = StringField(choices=cities)
    tickets = ListField(EmbeddedDocumentField('TicketModel'))
    user = EmbeddedDocumentField('UserModel')
    timestamp = DateTimeField(default=datetime.datetime.now)
    

    @property
    def serialize(self):        
        return {
            'id': self.id,
            'event_name': self.event_name,
            'event_description': self.event_description,
            'event_state': self.event_state,
            'event_city': self.event_city,
            'event_date': self.event_date.strftime('%m/%d/%Y'),
            'event_img': self.event_img,
            'count_tickets': len(self.tickets)
        }