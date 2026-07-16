[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $PythonArguments
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$bootstrap = Join-Path $PSScriptRoot 'runtime_bootstrap.py'
[Console]::Error.WriteLine(
    'DEPRECATED: scripts/python.ps1 is a compatibility shim; use tools/run.ps1 or tools/validate.ps1.'
)

if ($env:NARRATIVE_PYTHON) {
    $python = & $env:NARRATIVE_PYTHON $bootstrap --print-python
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $python = & py -3 $bootstrap --print-python
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $python = & python3 $bootstrap --print-python
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $python = & python $bootstrap --print-python
} else {
    Write-Error 'Python 3.11+ was not found. Install Python or set NARRATIVE_PYTHON.'
    exit 1
}
if ($LASTEXITCODE -ne 0 -or -not $python) {
    exit 1
}

& ($python.Trim()) @PythonArguments
exit $LASTEXITCODE
