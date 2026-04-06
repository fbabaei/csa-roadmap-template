Param(
    [Parameter(Mandatory = $false)]
    [int]$Port = 5500,

    [Parameter(Mandatory = $false)]
    [switch]$NoOpen
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$PortalScript = Join-Path $RepoRoot "scripts\start_portal.py"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $PortalScript)) {
    Write-Error "Could not find scripts/start_portal.py."
    exit 1
}

if (Test-Path $VenvPython) {
    $PythonCmd = $VenvPython
}
elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $PythonCmd = "py"
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
}
else {
    Write-Error "Python was not found. Install Python or create .venv first."
    exit 1
}

$args = @()
if ($PythonCmd -eq "py") {
    $args += "-3"
}
$args += @($PortalScript, "--port", "$Port")
if ($NoOpen) {
    $args += "--no-open"
}

Push-Location $RepoRoot
try {
    & $PythonCmd @args
}
finally {
    Pop-Location
}
