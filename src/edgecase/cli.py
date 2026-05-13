import json
import typer
from rich import print
from .models import Trace
from .registry import Registry
from .detectors import detect

app = typer.Typer(help="EdgeCase conflict-aware assurance CLI")

@app.command()
def run(
signals: str = typer.Option(..., help="Comma-separated signals"),
workflow: str = typer.Option("demo", help="Workflow name"),
):
trace = Trace(signals=[s.strip() for s in signals.split(",")], workflow=workflow)
report = detect(trace, Registry.default())
print(json.dumps(report.model_dump(), indent=2))

if name == "main":
app()
