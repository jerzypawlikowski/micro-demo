#!/usr/bin/env python
# -*- coding: utf-8 -*-
import aiozipkin as az
from aiohttp import ClientSession, web


async def fetch(session, url, ctx):
    async with session.get(url, trace_request_ctx=ctx) as response:
        return await response.json()


async def get(request):
    session = request.app["session"]
    span = az.request_span(request)
    ctx = {'span_context': span.context}
    response = await fetch(session, "http://backend:8081/", ctx)
    task_time = response["task_time"]
    return web.Response(text=f"The task was completed in: {task_time}")


async def make_app(host, port):
    app = web.Application()
    app.add_routes([web.get("/", get)])

    endpoint = az.create_endpoint("frontend", ipv4=host, port=port)
    zipkin_address = "http://zipkin:9411/api/v1/spans"
    tracer = await az.create(zipkin_address, endpoint, sample_rate=1.0)

    trace_config = az.make_trace_config(tracer)

    session = ClientSession(trace_configs=[trace_config])
    app["session"] = session

    async def close_session(app):
        await app["session"].close()

    app.on_cleanup.append(close_session)
    az.setup(app, tracer)
    return app


def run():
    host = "frontend"
    port = 8080
    app = make_app(host, port)
    web.run_app(app, port=port)


if __name__ == "__main__":
    run()
