#!/usr/bin/env bash
# Claude Code status line — colored version (ANSI safe attempt)

input=$(cat)

# Get current working directory from Claude
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd')
dir=$(basename "$cwd")

# ANSI colors (real ESC, not \033)
cyan="\x1b[36m"
blue="\x1b[34m"
red="\x1b[31m"
yellow="\x1b[33m"
green="\x1b[32m"
reset="\x1b[0m"

# Get git branch
branch=$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null)

# Build git info
if [ -n "$branch" ]; then
  if [ -n "$(git -C "$cwd" status --porcelain 2>/dev/null)" ]; then
    git_info=" ${blue}git:(${red}${branch}${blue}) ${yellow}✗${reset}"
  else
    git_info=" ${blue}git:(${red}${branch}${blue}) ${green}✔${reset}"
  fi
else
  git_info=""
fi

# Get 5-hour rate limit usage
five_pct=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
if [ -n "$five_pct" ]; then
  five_display=$(printf "%.0f" "$five_pct")
  rate_info=" ${yellow}5h:${five_display}%${reset}"
else
  rate_info=""
fi

# Get context window usage percentage
ctx_used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
if [ -n "$ctx_used" ]; then
  ctx_display=$(printf "%.0f" "$ctx_used")
  ctx_info=" ${green}ctx:${ctx_display}%${reset}"
else
  ctx_info=""
fi

# Output (use %b to interpret escape sequences)
printf "%b%b%b%b\n" "${cyan}${dir}${reset}" "$git_info" "$rate_info" "$ctx_info"