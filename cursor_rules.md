# Cursor "Ticket Driver" Prompt Template and Development Workflow

## Development Loop Workflow

1. Pick a ticket from the velocity backlog.
2. Scaffold minimal runnable code to satisfy acceptance criteria.
3. Commit and test locally.
4. Push and open PR for review.

Repeat for each ticket.

## Cursor Prompt Template

- Input: Ticket description, acceptance criteria, and current code context.
- Output: Minimal runnable code or tests addressing the ticket.
- Constraints: Keep code concise, testable, and aligned with MVP scope.

## Notes

- Prioritize backend API tickets first (OAuth, data fetching, scoring).
- Then implement frontend UI tickets (dashboard, settings).
- Use environment variables for secrets.
- Use SQLite for local dev.
- Use HTMX for simple dynamic UI interactions.
- Document all assumptions and next steps.
