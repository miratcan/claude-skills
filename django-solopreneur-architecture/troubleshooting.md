# Troubleshooting

## User Rejects Docker-Based Architecture

**Symptom**: User pushes back on Docker Compose, Kubernetes, or containerization proposals.

**Cause**: Assuming "modern" deployment without understanding user's context. Solo developers on small VPS often have limited memory, existing systemd setup, and no need for orchestration.

**Solution**:
1. Ask about existing infrastructure: "What's already running on your VPS?"
2. If they mention systemd/supervisor, propose that
3. Only suggest Docker if they specifically ask or have container experience

---

## User Insists on Django After FastAPI Proposal

**Symptom**: User corrects architecture proposal by insisting on Django.

**Solution**: Always check project preferences before proposing tech stack. If user says "always bet on Django" or similar, default to Django for all future proposals.
