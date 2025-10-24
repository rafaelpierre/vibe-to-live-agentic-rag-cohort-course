from agents import Runner, InputGuardrailTripwireTriggered
from src.agent.rag_agent import agent
from phoenix.otel import register
from openinference.semconv.trace import SpanAttributes
from openinference.instrumentation import OITracer
from opentelemetry.trace import StatusCode
from src.agent.models import AgentResponse


tracer_provider = register(
    project_name="fast_api_agent", auto_instrument=True, batch=True
)

tracer: OITracer = tracer_provider.get_tracer(
    instrumenting_module_name="opentelemetry.instrumentation.agents"
)


async def get_chat_response(prompt: str) -> AgentResponse:
    with tracer.start_as_current_span(
        "rag_agent", openinference_span_kind="chain"
    ) as span:
        try:
            span.set_attribute(SpanAttributes.INPUT_VALUE, prompt)
            result = await Runner.run(agent, prompt)
            span.set_attribute(SpanAttributes.OUTPUT_VALUE, str(result.final_output))
            span.set_status(StatusCode.OK)
            return result.final_output
        except InputGuardrailTripwireTriggered as tripwire:
            span.set_attribute(
                SpanAttributes.OUTPUT_VALUE, "Input guardrail tripwire triggered"
            )
            span.set_status(StatusCode.OK)
            return AgentResponse(
                answer="Sorry, I cannot answer that question as it is not related to economy.",
                sources=[],
            )
        except Exception as e:
            span.set_attribute(SpanAttributes.OUTPUT_VALUE, f"Error: {str(e)}")
            span.set_status(StatusCode.ERROR)
            return AgentResponse(answer=f"Error: {str(e)}", sources=[])
