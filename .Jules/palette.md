## 2025-05-14 - [Accessible Modals & Dynamic Feedback]
**Learning:** Single-file web interfaces often overlook ARIA roles and keyboard navigation for custom modals. Using `sr-only` for labels allows maintaining a minimalist aesthetic without sacrificing accessibility. Dynamic feedback on buttons during async operations significantly improves perceived performance.
**Action:** Always include `role="dialog"`, `aria-modal="true"`, and `Escape` key listeners for custom modals. Ensure every input has a linked `<label>`, even if visually hidden.
