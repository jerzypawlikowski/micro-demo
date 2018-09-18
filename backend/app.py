#!/usr/bin/env python
# -*- coding: utf-8 -*-
from asyncio import sleep
from random import random

from aiohttp import web


async def get(request):
    task_time = 2 * random()
    await sleep(task_time)
    return web.json_response(data={"task_time": task_time})

app = web.Application()
app.add_routes([
    web.get("/", get)
])

web.run_app(app, port=8081)
