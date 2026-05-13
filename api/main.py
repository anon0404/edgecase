from fastapi import FastAPI
from edgecase import Registry, Trace, detect

app = FastAPI(title="EdgeCase API", version="0.1.0")
registry = Registry.default()

@app.get("/")
def root():
return {
"name": "EdgeCase API",
"description": "Conflict-aware assurance for agentic systems",
}

@app.post("/v1/detect")
def detect_collision(trace: Trace):
return detect(trace, registry)
