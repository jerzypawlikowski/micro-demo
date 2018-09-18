#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiohttp import ClientSession, web


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def get(request):
    async with ClientSession() as session:
        response = await fetch(session, "http://backend:8081/")
    task_time = response["task_time"]
    return web.Response(text=f"The task was completed in: {task_time}")


app = web.Application()
app.add_routes([web.get("/", get)])

web.run_app(app, port=8080)
