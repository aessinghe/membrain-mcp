#!/usr/bin/env bash
# Regenerate the Membrain .mcpb (Desktop Extension) from the current state of
# this repo's src/. Run from anywhere; paths are resolved relative to this
# script's own location, so losing the staging folder never loses this tooling
# - only the main repo (this file included) needs to survive.
#
# Usage: mcpb/build.sh [staging_directory]
#   staging_directory defaults to a sibling folder ../Membrain-mcp-dxt-prototype
#   (created if missing) so distribution stays outside this git repo.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_REPO="$(dirname "$SCRIPT_DIR")"
STAGING="${1:-$MAIN_REPO/../Membrain-mcp-dxt-prototype}"

echo "1. Copying source from $MAIN_REPO to $STAGING"
mkdir -p "$STAGING"
cp "$MAIN_REPO/pyproject.toml" "$MAIN_REPO/uv.lock" "$MAIN_REPO/README.md" "$STAGING/"
rm -rf "$STAGING/src"
cp -r "$MAIN_REPO/src" "$STAGING/"
cp "$SCRIPT_DIR/manifest.json" "$SCRIPT_DIR/run.py" "$SCRIPT_DIR/.mcpbignore" "$STAGING/"

echo "2. Bumping version"
OLD_VERSION=$(grep -m1 '"version"' "$SCRIPT_DIR/manifest.json" | sed -E 's/.*"version":\s*"([^"]+)".*/\1/')
IFS='.' read -r MAJOR MINOR PATCH <<< "$OLD_VERSION"
NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
echo "   $OLD_VERSION -> $NEW_VERSION"

bump_json_version() {
    python - "$1" "$NEW_VERSION" <<'PYEOF'
import json, sys
path, version = sys.argv[1], sys.argv[2]
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
data["version"] = version
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")
PYEOF
}

# Bump the canonical, git-tracked manifest first (source of truth for next run),
# then copy it into the staging folder so both stay in sync.
bump_json_version "$SCRIPT_DIR/manifest.json"
cp "$SCRIPT_DIR/manifest.json" "$STAGING/manifest.json"

sed -i -E "s/^version = \".*\"\$/version = \"$NEW_VERSION\"/" "$STAGING/pyproject.toml"

echo "3. Cleaning + packing"
find "$STAGING/src" -iname "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
rm -f "$STAGING"/*.mcpb

(cd "$STAGING" && mcpb validate manifest.json && mcpb pack . "Membrain-mcp-dxt-prototype.mcpb")

echo ""
echo "Done. File: $STAGING/Membrain-mcp-dxt-prototype.mcpb (version $NEW_VERSION)"
echo "Manual step remaining: re-upload it via Organization Settings -> Connectors -> Desktop."
echo "Don't forget to commit the version bump in mcpb/manifest.json in this repo."
