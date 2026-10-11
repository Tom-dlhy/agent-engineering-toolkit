# Provider capability matrix and streaming envelopes

**Read when:** mapping OpenAI/Azure, AWS Converse or Gemini-native
structured output, streaming, function tools and multimodal blocks.

## Features to verify for the exact deployment
Tool schema/tool ID, JSON mode vs strict schema, supported schema
subset, reasoning/safety/refusal content, token usage, prompt
caching, multimodal inputs, regional availability, rate limits,
stream tool-call assembly and model/version-specific constraints.
A common SDK wrapper doesn't make unsupported model features
available. Tool arguments are suggestions requiring runtime
validation and authorization by the application.

AWS ConverseStream emits messageStart, contentBlockStart/Delta/Stop,
messageStop and metadata. Deltas can be partial JSON for tool
arguments; usage may arrive at the end. Signed model reasoning
blocks may require the unchanged preceding history. A stream
that disconnects before terminal stop must not be reported as
complete, valid structured data.

## Verification
Record tested SDK/endpoint/model ID/region and response fixtures.
Simulate refusals, unsupported schema, parallel tool calls,
missing tool IDs, malformed arguments, partial stream,
truncation and absent usage. Pin adapters and use provider-native
sandbox only when authorized. Never claim that temperature zero
makes outputs perfectly reproducible.

Sources: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html ,
https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling ,
https://platform.openai.com/docs/guides/structured-outputs .
