<#
.SYNOPSIS
  Regenerate the Membrain .mcpb (Desktop Extension) from the current state of
  this repo's src/. Equivalent to build.sh, for a plain Windows PowerShell setup.

.PARAMETER Staging
  Destination folder (created if missing). Defaults to a sibling folder
  ..\Membrain-mcp-dxt-prototype, kept outside this git repo.
#>
param(
    [string]$Staging
)

$ErrorActionPreference = "Stop"

$ScriptDir = $PSScriptRoot
$MainRepo = Split-Path $ScriptDir -Parent
if (-not $Staging) {
    $Staging = Join-Path (Split-Path $MainRepo -Parent) "Membrain-mcp-dxt-prototype"
}

Write-Host "1. Copying source from $MainRepo to $Staging" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $Staging | Out-Null
Copy-Item "$MainRepo\pyproject.toml", "$MainRepo\uv.lock", "$MainRepo\README.md" -Destination $Staging -Force
Remove-Item "$Staging\src" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item "$MainRepo\src" -Destination $Staging -Recurse -Force
Copy-Item "$ScriptDir\manifest.json", "$ScriptDir\run.py", "$ScriptDir\.mcpbignore" -Destination $Staging -Force

Write-Host "2. Bumping version" -ForegroundColor Cyan
$manifest = Get-Content "$ScriptDir\manifest.json" -Raw | ConvertFrom-Json
$oldVersion = $manifest.version
$parts = $oldVersion.Split(".")
$parts[2] = [int]$parts[2] + 1
$newVersion = $parts -join "."
Write-Host "   $oldVersion -> $newVersion"

# Delegate the actual file writes to Python (json.dump always writes clean
# UTF-8 without a BOM) - Set-Content/-Encoding utf8 in Windows PowerShell
# writes a BOM that mcpb's JSON parser rejects; this sidesteps that entirely,
# and keeps the same version-bumping logic as build.sh.
python -c @"
import json
path = r'$ScriptDir\manifest.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
data['version'] = '$newVersion'
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')
"@

Copy-Item "$ScriptDir\manifest.json" "$Staging\manifest.json" -Force

(Get-Content "$Staging\pyproject.toml" -Raw) -replace '(?m)^version = ".*"$', "version = `"$newVersion`"" |
    python -c "import sys; open(r'$Staging\pyproject.toml', 'w', encoding='utf-8', newline='').write(sys.stdin.read())"

Write-Host "3. Cleaning + packing" -ForegroundColor Cyan
Get-ChildItem "$Staging\src" -Recurse -Filter "__pycache__" -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Remove-Item "$Staging\*.mcpb" -Force -ErrorAction SilentlyContinue

Push-Location $Staging
try {
    mcpb validate manifest.json
    mcpb pack . "Membrain-mcp-dxt-prototype.mcpb"
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "Done. File: $Staging\Membrain-mcp-dxt-prototype.mcpb (version $newVersion)" -ForegroundColor Green
Write-Host "Manual step remaining: re-upload it via Organization Settings -> Connectors -> Desktop." -ForegroundColor Yellow
Write-Host "Don't forget to commit the version bump in mcpb\manifest.json in this repo." -ForegroundColor Yellow
