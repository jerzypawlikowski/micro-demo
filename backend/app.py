#!/usr/bin/env python
# -*- coding: utf-8 -*-
from asyncio import sleep
from random import random

import aiozipkin as az
from aiohttp import web


async def get(request):
    task_time = random()
    await sleep(task_time)
    return web.json_response(data={"task_time": task_time})


async def make_app(host, port):
    app = web.Application()
    app.add_routes([web.get("/", get)])

    endpoint = az.create_endpoint("backend", ipv4=host, port=port)
    zipkin_address = "http://zipkin:9411/api/v1/spans"
    tracer = await az.create(zipkin_address, endpoint, sample_rate=1.0)
    az.setup(app, tracer)
    return app


def run():
    host = "backend"
    port = 8081
    app = make_app(host, port)
    web.run_app(app, port=port)


if __name__ == "__main__":
    run()

