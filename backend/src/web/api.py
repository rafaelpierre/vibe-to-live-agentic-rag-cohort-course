from fastapi import FastAPI
from pydantic import BaseModel
from agents import Runner
from src.agents.rag_agent import agent
from src.agents.models import AgentResponse
from phoenix.otel import register
from openinference.semconv.trace import SpanAttributes
from openinference.instrumentation import OITracer
from opentelemetry.trace import StatusCode

app = FastAPI()

tracer_provider = register(
  project_name="fast_api_agent",
  auto_instrument=True,
  batch=True
)

tracer: OITracer = tracer_provider.get_tracer(instrumenting_module_name = "opentelemetry.instrumentation.agents")

class ChatRequest(BaseModel):
    message: str


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/chat")
async def chat(request: ChatRequest) -> AgentResponse:
    
        with tracer.start_as_current_span(
            "rag_agent",
            openinference_span_kind="chain"
        ) as span:
            try:
                span.set_attribute(SpanAttributes.INPUT_VALUE, request.message)
                result = await Runner.run(agent, request.message)
                span.set_attribute(SpanAttributes.OUTPUT_VALUE, str(result.final_output))
                span.set_status(StatusCode.OK)
                return result.final_output
            except Exception as e:
                span.set_attribute(SpanAttributes.OUTPUT_VALUE, f"Error: {str(e)}")
                span.set_status(StatusCode.ERROR)
