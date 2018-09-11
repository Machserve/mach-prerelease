# -*- coding: utf-8 -*-

import asyncio
import concurrent.futures

from google.cloud import firestore

from mach_prerelease.models.firestore_document import FirestoreDocument


class FirestoreConnector(object): 
	"""Authenticated Google FireStore object with methods to access Firestore.

	See Also
	---------
	https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/client.html
	https://cloud.google.com/firestore/docs/quickstart-servers
	"""
	def __init__(self):
		self.db = firestore.Client()


	def validate_email(self, email: str) -> bool:
		"""Check if the email already exists in the collection.

		Parameters
		----------
		email : str
			The email to be validated
		
		Returns
		-------
		bool
			True if the email exists
			False if the email does not exist
		"""
		documents = self.db.collection("prospectives").get()
		emails = []
		for document in documents:
			emails.append(document.to_dict()["email"])
		print(emails)
		if email in emails:
			return False
		return True


	def add_document(self, data: dict) -> None:
		"""Add the data of a new prospective customer.

		Parameters
		----------
		data : FirestoreDocument
		"""
		self.db.collection("prospectives").document().set(data)
