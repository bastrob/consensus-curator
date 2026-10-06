CREATE TABLE IF NOT EXISTS topics (
    slug TEXT PRIMARY KEY,
    label TEXT NOT NULL
);

INSERT INTO topics (slug, label) VALUES
    ('ai-agents', 'AI agents and multi-agent systems'),
    ('coding-assistants', 'AI coding assistants and copilots'),
    ('llm-research', 'LLM research, architectures and model releases'),
    ('ai-safety', 'AI safety and alignment'),
    ('ai-policy', 'AI policy, regulation and governance'),
    ('ai-infrastructure', 'AI training and inference infrastructure'),
    ('generative-ai', 'Generative AI for image, video and audio'),
    ('ai-business', 'AI adoption, funding and enterprise applications')
ON CONFLICT (slug) DO NOTHING
;