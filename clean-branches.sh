#!/usr/bin/env bash
# clean-branches.sh — delete local git branches already merged into main/master
# Usage: ./clean-branches.sh [base-branch]

set -euo pipefail

BASE=${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||' || echo "main")}

echo "Cleaning branches merged into '$BASE'..."
echo

DELETED=0
KEPT=0

while IFS= read -r branch; do
  branch=$(echo "$branch" | xargs)  # trim whitespace
  if [[ "$branch" == "$BASE" || "$branch" == "main" || "$branch" == "master" || "$branch" == "dev" ]]; then
    echo "  kept:    $branch (protected)"
    ((KEPT++))
    continue
  fi
  git branch -d "$branch"
  echo "  deleted: $branch"
  ((DELETED++))
done < <(git branch --merged "$BASE" | grep -v "^\*")

echo
echo "Done. Deleted $DELETED branch(es), kept $KEPT protected branch(es)."
