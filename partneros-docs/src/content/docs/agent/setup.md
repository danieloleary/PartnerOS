---

title: Setup Guide
description: PartnerOS template
---

## Troubleshooting

### "anthropic package not installed"

```bash
pip install anthropic
```

### "ANTHROPIC_API_KEY not set"

Make sure you've exported the key in your current terminal session:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# Verify
echo $ANTHROPIC_API_KEY
```

### "ModuleNotFoundError: No module named 'rich'"

Rich is optional but recommended:

```bash
pip install rich
```

### Permission Denied on agent.py

```bash
chmod +x agent.py
```
