param(
    [ValidateSet("Plan", "RetrieveBoundary", "RetrieveDem", "Derive", "BuildProject", "Verify", "Open")]
    [string]$Action = "Plan",
    [string]$OsgeoRoot = "D:\"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = Join-Path $repoRoot "runtime_data\qgis\cooma_spatial_foundation"
$projectPath = Join-Path $workspaceRoot "project\Cooma_Spatial_Foundation_v0_2_terrain.qgz"
$pythonPath = Join-Path $OsgeoRoot "bin\python.exe"
$qgisLauncher = Join-Path $OsgeoRoot "bin\qgis-ltr.bat"

if ($Action -eq "Open") {
    if (-not (Test-Path -LiteralPath $projectPath -PathType Leaf)) {
        throw "Terrain QGIS project not found: $projectPath"
    }
    & $qgisLauncher $projectPath
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

$actionMap = @{
    Plan = "plan"
    RetrieveBoundary = "retrieve-boundary"
    RetrieveDem = "retrieve-dem"
    Derive = "derive"
    BuildProject = "build-project"
    Verify = "verify"
}
$moduleAction = $actionMap[$Action]
& $pythonPath -u -m cczps_lite.qgis_local_spatial_foundation.terrain_pack $moduleAction --osgeo-root $OsgeoRoot
if ($LASTEXITCODE -ne 0) {
    throw "QGIS Cooma terrain pack $moduleAction failed with exit code $LASTEXITCODE"
}
