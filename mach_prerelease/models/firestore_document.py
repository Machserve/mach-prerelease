# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class FirestoreDocument(Schema):
    """Represents a document in the 'prospectives' Google Firestore collection
    
    Attributes
    ----------
    email : str
        The email of the prospective customer.
    ip_address : str
        The IPv4 address of the prospective customer.
    port : int
        The aiohttp port that the prospective customer accessed the application from.
    submit_time : datetime.datetime
        The time that the prospective customer submitted the form.
    """
    email = fields.Str()
    ip_address = fields.Str()
    port = fields.Integer()
    submit_time = fields.Date()
