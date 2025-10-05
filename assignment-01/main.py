from fastapi import FastAPI
from agents import Runner
from rag_agent import create_rag_agent

app = FastAPI()

@app.get("/ask")
async def ask_agent(question: str):
    result = await Runner.run(create_rag_agent(), question)
    return {"answer": result.final_output}
