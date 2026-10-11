# Hexagonal Python: protocol ports and composition

**Read when:** isolating testable application behavior from external services and connecting implementations at runtime.

~~~python
from typing import Protocol

class TextGenerator(Protocol):
    async def generate(self, *, instruction: str) -> str: ...

class ReportService:
    def __init__(self, generator: TextGenerator) -> None:
        self.generator = generator

    async def build(self, topic: str) -> str:
        if not topic.strip():
            raise ValueError("topic must not be empty")
        return await self.generator.generate(instruction=f"Summarize: {topic}")
~~~

The service has no OpenAI, Bedrock, Google, LiteLLM or FastAPI dependency. At composition root choose BedrockTextGenerator or other adapter, with app-owned config and lifespan resource; do not put imports and credentials into domain module. Untrusted model output is **not** safely validated merely because returned as str; validate contract separately.

## Port decision
Abstract by *business behavior*, not every vendor method: `save_invoice` instead of `put_object` when implementation changes don't belong in application layer. When service has one concrete stable dependency and no test difficulty, injecting concrete class is often enough.

## Failure ownership
Domain errors belong inside domain, infrastructure errors translated in adapter (without false 404/503 equivalence), HTTP status codes only in transport. Observe and close clients at lifecycle boundary.

## Governance
Avoid generating a dozen empty folders or DI framework simply to satisfy "clean architecture". Keep imports pointing inward and enforce with a small architecture test if mature enough.

Source: https://www.cosmicpython.com/ and https://docs.python.org/3/library/typing.html .
