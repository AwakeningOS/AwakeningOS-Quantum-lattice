#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .git ]; then
  echo "error: run this from the repository root" >&2
  exit 1
fi

mkdir -p .git/hooks
cat > .git/hooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail
python scripts/check_raw_logs.py
HOOK
chmod +x .git/hooks/pre-commit

echo "Installed .git/hooks/pre-commit -> python scripts/check_raw_logs.py"
