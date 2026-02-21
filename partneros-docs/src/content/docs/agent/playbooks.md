---

title: Playbooks
description: PartnerOS template
---

## Creating Custom Playbooks

Add new playbooks by creating YAML files in `playbooks/`:

```yaml
name: Partner Renewal
description: Annual partnership renewal process
steps:
  - template: III_Partner_Enablement_Templates/06-success-metrics.md
    name: Review Metrics
    prompt: |
      Review the partner's performance over the past year.

  - template: III_Partner_Enablement_Templates/07_Partner_QBR_Template.md
    name: Renewal Discussion
    prompt: |
      Prepare talking points for the renewal conversation.
```

See [Configuration](configuration.md) for more customization options.
