
"""
AsyncServer
----------

A server built with `asyncio` and `sockets`.

Example:
```python3.10
from nsgi.application import AsyncServer
from nsgi.runner import Runner
from nsgi.responses import Response

server = AsyncServer()
runner = Runner(server)

@server.route("/", method="GET")
async def index():
	return Response("Hello.")

runner.run()
```

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

from .application import AsyncServer
from .runner import Runner
from .responses import (JSONResponse, Response, HTMLResponse)
from .route import Route
from .models import *

__version__ = "1.0.4"