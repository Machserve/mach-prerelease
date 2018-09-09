# -*- coding: utf-8 -*-

"""Custom decorator functions."""

import atexit

from contextlib import redirect_stderr, redirect_stdout
from functools import wraps
from threading import Thread
from typing import Callable


def thread_task(f: Callable) -> Callable:
	"""Defines a wrapper that will decorate a function.
	
	Parameters
	----------
	f : Callable
		The function to be wrapped.

	Returns
	-------
	Callable
		A function that will be ran on a seperate thread when it is called.
	"""
	@wraps(f)
	def wrapper(*args, **kwargs):
		thread = Thread(target=f, name=f.__name__, args=args, kwargs=kwargs)
		thread.daemon = True
		thread.start()
	return wrapper

