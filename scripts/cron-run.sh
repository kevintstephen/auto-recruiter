#!/usr/bin/env bash
# Weekly recruiting pipeline run — designed for cron (Friday 2pm) or manual use.
# Manual: ./scripts/cron-run.sh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$REPO_DIR/runs/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d_%H%M).log"

# Cron has a minimal PATH; resolve claude explicitly.
CLAUDE_BIN="${CLAUDE_BIN:-$(command -v claude || echo "$HOME/.local/bin/claude")}"

cd "$REPO_DIR"

"$CLAUDE_BIN" -p "/weekly-run" \
  --allowedTools "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Bash(curl *),Bash(date *),Bash(mkdir *),mcp__gmail__search_threads,mcp__gmail__get_thread,mcp__gmail__create_draft,mcp__notion__*,mcp__gdrive__search_files,mcp__gdrive__read_file_content" \
  --max-turns 80 \
  --output-format json \
  >> "$LOG_FILE" 2>&1

echo "Run complete: $LOG_FILE"
