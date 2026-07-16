[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $RunArguments
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $repoRoot 'tools\run_repo.py'

if ($env:NARRATIVE_PYTHON) {
    & $env:NARRATIVE_PYTHON $runner @RunArguments
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $runner @RunArguments
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 $runner @RunArguments
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python $runner @RunArguments
} else {
    Write-Error 'Python 3.11+ was not found. Install Python or set NARRATIVE_PYTHON.'
    exit 1
}
exit $LASTEXITCODE
