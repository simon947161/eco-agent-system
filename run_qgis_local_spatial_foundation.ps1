param(
    [ValidateSet("Build", "Revise", "Verify", "Open")]
    [string]$Action = "Verify",
    [string]$OsgeoRoot = "D:\"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = Join-Path $repoRoot "runtime_data\qgis\cooma_spatial_foundation"
$baseProjectPath = Join-Path $workspaceRoot "project\Cooma_Spatial_Foundation_v0_1.qgz"
$revisionProjectPath = Join-Path $workspaceRoot "project\Cooma_Spatial_Foundation_v0_1_ux_revision.qgz"
$projectPath = if (Test-Path -LiteralPath $revisionProjectPath -PathType Leaf) {
    $revisionProjectPath
} else {
    $baseProjectPath
}
$pythonPath = Join-Path $OsgeoRoot "bin\python.exe"
$qgisPath = Join-Path $OsgeoRoot "bin\qgis-ltr-bin.exe"

if ($Action -eq "Open") {
    if (-not (Test-Path -LiteralPath $projectPath -PathType Leaf)) {
        throw "QGIS project not found. Run with -Action Build first: $projectPath"
    }
    Start-Process -FilePath $qgisPath -ArgumentList @($projectPath)
    return
}

if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
    throw "QGIS-bundled Python not found: $pythonPath"
}

$env:PYTHONHOME = Join-Path $OsgeoRoot "apps\Python312"
$env:PYTHONPATH = Join-Path $OsgeoRoot "apps\qgis-ltr\python"
$env:QGIS_PREFIX_PATH = (Join-Path $OsgeoRoot "apps\qgis-ltr").Replace("\", "/")
$env:QT_PLUGIN_PATH = @(
    (Join-Path $OsgeoRoot "apps\qgis-ltr\qtplugins"),
    (Join-Path $OsgeoRoot "apps\Qt5\plugins")
) -join ";"
$env:GDAL_DATA = Join-Path $OsgeoRoot "apps\gdal\share\gdal"
$env:PROJ_DATA = Join-Path $OsgeoRoot "share\proj"

$moduleAction = $Action.ToLowerInvariant()
& $pythonPath -u -m cczps_lite.qgis_local_spatial_foundation.project_builder $moduleAction --osgeo-root $OsgeoRoot
if ($LASTEXITCODE -ne 0) {
    throw "QGIS local spatial foundation $moduleAction failed with exit code $LASTEXITCODE"
}
