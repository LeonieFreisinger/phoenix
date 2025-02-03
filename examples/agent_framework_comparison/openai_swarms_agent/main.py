import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import gradio as gr
from openinference.semconv.trace import SpanAttributes
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from router import SwarmRouter
from utils.instrument import Framework, instrument


def gradio_interface(message, history):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("openai_swarms_agent") as span:
        span.set_attribute(SpanAttributes.INPUT_VALUE, message)
        span.set_attribute(SpanAttributes.OPENINFERENCE_SPAN_KIND, "AGENT")

        context = {}
        TraceContextTextMapPropagator().inject(context)
        
        router = SwarmRouter()
        agent_response = router.process_query(message, context)
        
        span.set_attribute(SpanAttributes.OUTPUT_VALUE, agent_response)
        span.set_status(trace.Status(trace.StatusCode.OK))
        return agent_response


def launch_app():
    iface = gr.ChatInterface(fn=gradio_interface, title="OpenAI Swarms Agent")
    iface.launch()


if __name__ == "__main__":
    instrument(project_name="openai-swarms-agent", framework=Framework.OPENAI_SWARMS)
    launch_app() 