# Paste the file or let Claude Code find it? Half the tokens, 13% of the money.

*Draft. Tech in General experiment #015. 24 headless Claude Code runs (Opus 5.5, Pro), 2026-10-15 IST.*

Six small bugs in a folder of 14 JavaScript packages. Two ways to ask:

- **Bare:** "Bug report: the duration parser ignores seconds. Find it and fix it."
- **Front-loaded:** the same, plus the file path, the test command, and both files pasted into the prompt.

Every run fixed its bug either way.

| | Bare | Front-loaded |
|---|---|---|
| Total tokens | 78K | 43K (−45%) |
| Tool calls | 3.3 | 1.4 |
| Est. cost per task | 11.8¢ | 10.2¢ (−13.5%) |

**Why the token cut didn't turn into the same cost cut.** Each extra model call re-sends Claude Code's ~11–16K-token system prefix, but from cache at 1/20th of the input price. So the exploring calls are token-heavy and cheap. The files you paste go in as fresh tokens that Claude Code writes to its 1-hour cache at twice the input price.

**Where it paid off.** The bugs that took the most finding (median: −35%, durations: −27%). On two tasks the saving was zero because Claude still ran the test twice.

**Fun detail.** Claude Code never used its Read tool to look around. It used `ls`, `cat` and `grep` in Bash.

**Takeaway.** Tell it where the bug is and how to check: it's faster (15 s → 11 s) and a bit cheaper. Don't expect the 45% token drop to show up on the bill.

*$ are API-equivalent estimates from Claude Code's `total_cost_usd`; Pro isn't billed per token.*
