[CmdletBinding()]
param()

$repoRoot = Split-Path -Parent $PSScriptRoot
$validator = Join-Path $repoRoot 'tools\validate_repo.py'

if ($env:NARRATIVE_PYTHON) {
    & $env:NARRATIVE_PYTHON $validator
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $validator
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 $validator
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python $validator
} else {
    Write-Error 'Python 3.11+ was not found. Install Python or set NARRATIVE_PYTHON.'
    exit 1
}
exit $LASTEXITCODE
