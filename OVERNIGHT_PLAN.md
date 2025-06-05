---
title: Overnight Plan for Markdown Keyword Improvements
keywords: ["major headings add", "keywords field under", "content enhancement suggestions", "markdown keyword improvements", "plan outlines steps", "improve keyword metadata"]
---
# Overnight Plan for Markdown Keyword Improvements

This plan outlines steps to improve keyword metadata for all Markdown files in the repository and to analyze the four files with the least content. Improvements will run overnight via automation.

## 1. Inventory All Markdown Files
- Use `find` to list every `*.md` file.
- Record paths in a CSV for tracking.

## 2. Update Front‑Matter Keywords
- For files that already contain YAML front matter (`---` block):
  - Parse the `title` and `description` fields.
  - Generate 4–6 descriptive keywords based on those fields and major headings.
  - Add or update a `keywords:` field under the existing metadata.
- For files without front matter:
  - Extract the first heading as the `title`.
  - Create a minimal front matter block including `title` and generated `keywords`.
- Save modified files back in place.

## 3. Analyze Markdown Lengths
- Compute word counts for all Markdown files.
- Identify the four shortest files:
  1. `partner_blueprint/III_Partner_Enablement_Templates/README.md`
  2. `partner_blueprint/II_Partner_Recruitment_Templates.md`
  3. `partner_blueprint/II_Partner_Recruitment_Templates/README.md`
  4. `partner_blueprint/I_Partner_Strategy_Templates/README.md`
- These small files likely have limited context for keyword generation and content.

## 4. Enhancement Suggestions for Worst Four
- Expand introductory paragraphs to describe the purpose of each folder or section.
- Include 4–6 targeted keywords summarizing the main concepts (e.g., "partner enablement," "email outreach," "partner strategy").
- Consider adding a brief summary or bullet list of contents to improve searchability.

## 5. Automation Schedule
- Run a script overnight to apply the keyword updates and record modifications in git.
- Verify each file's front matter is valid YAML.
- Commit changes for review the next morning.
