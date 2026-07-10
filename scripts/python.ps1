[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $PythonArguments
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $repoRoot '.venv\Scripts\python.exe'

if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
    Write-Error @"
Repository Python was not found at:
  $venvPython

Create the environment with Python 3.10 or newer, then install test tooling:
  py -3 -m venv .venv
  .\.venv\Scripts\python.exe -m pip install -e ".[test]"
"@
    exit 1
}

& $venvPython @PythonArguments
exit $LASTEXITCODE
