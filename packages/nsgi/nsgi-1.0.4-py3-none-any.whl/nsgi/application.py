"""
MIT License

Copyright (c) 2022-present OpenRobot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import asyncio
import typing

from .route import Route

__all__ = ("AsyncServer",)

class AsyncServer(object):
	"""A server you can run with the `Runner` class

	This class makes a pre-made server object and makes it simple to subclass and add features to it.\n
	Any contributions to the github is appreciated.
	
	"""
	def __init__(self) -> None:
		self.loop = asyncio.get_event_loop()
		self.routes = {}

	def route(self, path : str, method : str = "GET"):
		def wrapper(func : typing.Callable):
			self.routes[path] = Route(path, func, method)
		return wrapper

	def get(self, path : str, method : str = "GET"):
		def wrapper(func : typing.Callable):
			self.routes[path] = Route(path, func, method)
		return wrapper

	def patch(self, path : str, method : str = "PATCH"):
		def wrapper(func : typing.Callable):
			self.routes[path] = Route(path, func, method)
		return wrapper

	def post(self, path : str, method : str = "POST"):
		def wrapper(func : typing.Callable):
			self.routes[path] = Route(path, func, method)
		return wrapper