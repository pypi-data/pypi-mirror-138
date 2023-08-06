import os
import logging

import beeline
from beeline.trace import unmarshal_trace_context

ENV_WRITEKEY = "GLOBAL_HONEYCOMB_API_KEY"
ENV_DATASET = "GLOBAL_HONEYCOMB_DATASET"
ENV_HOST = "GLOBAL_HONEYCOMB_HOST"
ENV_NAMESPACE = "NAMESPACE"

HEADER_TRACE_CONTEXT = 'X-Honeycomb-Trace'

logger = logging.getLogger(__name__)


def init_tracing(service_name):
    logger = logging.getLogger(__name__)

    api_key = os.getenv(ENV_WRITEKEY, "")
    if api_key == "":
        logger.warning(f'{ENV_WRITEKEY} not set. Tracing disabled.')
        return

    dataset = os.getenv(ENV_DATASET, "")
    if dataset == "":
        logger.warning(f'{ENV_DATASET} not set. Tracing disabled.')
        return

    host = os.getenv(ENV_HOST, "")
    if host == "":
        host = 'https://api.honeycomb.io'
    else:
        namespace = os.getenv(ENV_NAMESPACE)
        if namespace != "":
            host = host.replace("${NAMESPACE}", namespace)

    beeline.init(
        writekey=api_key,
        dataset=dataset,
        service_name=service_name,
        api_host=host,
    )
    logger.info(f'Honeycomb tracing enabled. Traces will be available in the dataset {dataset} and sent to host {host}')


def span_from_request_headers(headers, new_span_name):
    """
    Given tornado request headers, look for trace propagation info.
    Open and a return a child span if yes, otherwise return None.
    """
    trace_context = headers.get(HEADER_TRACE_CONTEXT, None)

    if trace_context is not None:
        trace_id, parent_id, context = unmarshal_trace_context(trace_context)

        context = {
            'name': new_span_name,
            **context
        }

        return beeline.start_trace(context=context, trace_id=trace_id, parent_span_id=parent_id)

    trace = beeline.start_trace(context={
        "name": new_span_name,
    })
    beeline.add_trace_field("namespace", os.getenv(ENV_NAMESPACE, ""))
    return trace


def tracing_context_from_handler(handler):
    """
    Extracts some info from a tornado.web.RequestHandler and returns a map
    suitable for use with beeline's add_context().
    Only call as the request is returning, otherwise duration_ms will be off.

    Since contract-vm uses sanic instead of Tornado, this is only used by mock network.
    Consider it deprecated.
    """
    return {
        "name": handler.request.uri,
        "duration_ms": handler.request.request_time() * 1000.0,
        "request.method": handler.request.method,
        "request.remote_addr": handler.request.remote_ip,
        "request.path": handler.request.uri,
        "request.query": handler.request.query,
        "request.host": handler.request.headers.get('Host'),
        "response.status_code": handler.get_status(),
    }
