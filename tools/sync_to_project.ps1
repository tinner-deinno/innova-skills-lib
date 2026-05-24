#Requires -Version 5.1
<#
.SYNOPSIS
    Syncs skills from the global ~/.claude/skills/ into any project's .claude/skills/ directory.

.DESCRIPTION
    Iterates every top-level directory under the global skills root and creates either a
    Windows Directory Junction (default, zero disk duplication) or a full recursive copy
    into the target project's .claude/skills/ folder.

    The special 'ecc' directory is handled separately: each sub-skill inside ecc/ is linked
    or copied as a flat 'ecc-<subname>' entry â€" matching the naming convention already used
    by innova-bot and the harness skill loader.

.PARAMETER ProjectPath
    Absolute path to the project root.  The script targets <ProjectPath>\.claude\skills\.
    Example: "C:\Users\MDES-DEV-NB\innova-bot"

.PARAMETER SourceRoot
    Override the global skills source directory.
    Default: $env:USERPROFILE\.claude\skills

.PARAMETER Mode
    'junction' (default) â€" create NTFS directory junctions (fast, zero copy, requires no
                            elevation on Windows 10/11 with Developer Mode or admin rights).
    'copy'     â€" perform a full recursive copy (useful for CI, containers, or network paths
                 that do not support junctions).

.PARAMETER DryRun
    Print every action that WOULD be taken without actually creating junctions or copying files.

.PARAMETER Force
    Overwrite / recreate entries that already exist.
    For junction mode: removes the old junction and creates a new one.
    For copy mode: deletes the target directory and re-copies.

.EXAMPLE
    .\sync_to_project.ps1 -ProjectPath "C:\Users\MDES-DEV-NB\innova-bot"

.EXAMPLE
    .\sync_to_project.ps1 -ProjectPath "C:\Users\MDES-DEV-NB\my-project" -Mode copy

.EXAMPLE
    .\sync_to_project.ps1 -ProjectPath "C:\Users\MDES-DEV-NB\innova-bot" -DryRun

.EXAMPLE
    .\sync_to_project.ps1 -ProjectPath "C:\Users\MDES-DEV-NB\innova-bot" -Force
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory = $true, HelpMessage = "Absolute path to the project root")]
    [string]$ProjectPath,

    [string]$SourceRoot = "$env:USERPROFILE\.claude\skills",

    [ValidateSet('junction', 'copy')]
    [string]$Mode = 'junction',

    [switch]$DryRun,

    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

function Write-Log {
    param([string]$Level, [string]$Message, [ConsoleColor]$Color = 'White')
    $ts = Get-Date -Format 'HH:mm:ss'
    Write-Host "[$ts] $Level  $Message" -ForegroundColor $Color
}

function Write-OK    { param([string]$m) Write-Log 'OK   ' $m Green }
function Write-Skip  { param([string]$m) Write-Log 'SKIP ' $m DarkGray }
function Write-Warn  { param([string]$m) Write-Log 'WARN ' $m Yellow }
function Write-Err   { param([string]$m) Write-Log 'ERROR' $m Red }
function Write-Dry   { param([string]$m) Write-Log 'DRY  ' $m Magenta }
function Write-Info  { param([string]$m) Write-Log 'INFO ' $m Cyan }

$script:Created = 0
$script:Skipped = 0
$script:Errors  = 0

# ---------------------------------------------------------------------------
# Core action: create one entry (junction or copy) at $LinkPath -> $TargetPath
# ---------------------------------------------------------------------------

function Sync-Entry {
    param(
        [string]$LinkPath,    # destination inside project .claude/skills/
        [string]$TargetPath,  # source directory to link to / copy from
        [string]$DisplayName  # label for log output
    )

    $exists = Test-Path $LinkPath

    if ($exists -and -not $Force) {
        Write-Skip $DisplayName
        $script:Skipped++
        return
    }

    if ($DryRun) {
        if ($exists) {
            Write-Dry "$DisplayName  [would recreate ($Mode)]"
        } else {
            Write-Dry "$DisplayName  [would create ($Mode)]"
        }
        $script:Created++
        return
    }

    # Remove existing entry when -Force
    if ($exists) {
        try {
            $item = Get-Item $LinkPath -Force
            if ($item.LinkType -eq 'Junction' -or $item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                # Remove junction without touching the source
                cmd /c "rmdir `"$LinkPath`"" 2>$null | Out-Null
            } else {
                Remove-Item $LinkPath -Recurse -Force
            }
        } catch {
            Write-Err "$DisplayName  (failed to remove existing: $_)"
            $script:Errors++
            return
        }
    }

    try {
        if ($Mode -eq 'junction') {
            New-Item -ItemType Junction -Path $LinkPath -Target $TargetPath -ErrorAction Stop | Out-Null
            Write-OK "$DisplayName  -> [junction] $TargetPath"
        } else {
            Copy-Item -Path $TargetPath -Destination $LinkPath -Recurse -Force -ErrorAction Stop
            Write-OK "$DisplayName  -> [copy] $TargetPath"
        }
        $script:Created++
    } catch {
        Write-Err "$DisplayName  ($_)"
        $script:Errors++
    }
}

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

if (-not (Test-Path $ProjectPath -PathType Container)) {
    Write-Error "ProjectPath does not exist or is not a directory: $ProjectPath"
    exit 1
}

if (-not (Test-Path $SourceRoot -PathType Container)) {
    Write-Error "SourceRoot does not exist: $SourceRoot"
    exit 1
}

$TargetRoot = Join-Path $ProjectPath '.claude\skills'

# Ensure destination exists
if (-not (Test-Path $TargetRoot)) {
    if ($DryRun) {
        Write-Dry "Would create directory: $TargetRoot"
    } else {
        New-Item -ItemType Directory -Path $TargetRoot -Force | Out-Null
        Write-Info "Created directory: $TargetRoot"
    }
}

# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " sync_to_project.ps1" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Source : $SourceRoot"
Write-Host " Target : $TargetRoot"
Write-Host " Mode   : $Mode"
if ($DryRun) { Write-Host " DRY RUN -- no changes will be made" -ForegroundColor Magenta }
if ($Force)  { Write-Host " FORCE   -- existing entries will be overwritten" -ForegroundColor Yellow }
Write-Host ""

# ---------------------------------------------------------------------------
# Pass 1 -- Top-level skill directories (skip 'ecc', handled separately)
# ---------------------------------------------------------------------------

Write-Info "--- Top-level skills ---"

$topLevel = Get-ChildItem $SourceRoot -Directory -ErrorAction Stop |
            Where-Object { $_.Name -ne 'ecc' }

foreach ($dir in $topLevel) {
    Sync-Entry `
        -LinkPath    (Join-Path $TargetRoot $dir.Name) `
        -TargetPath  $dir.FullName `
        -DisplayName $dir.Name
}

# ---------------------------------------------------------------------------
# Pass 2 â€" ecc sub-skills: flatten as ecc-<subname>
# ---------------------------------------------------------------------------

$eccSource = Join-Path $SourceRoot 'ecc'

if (Test-Path $eccSource -PathType Container) {
    Write-Host ""
    Write-Info "--- ecc sub-skills  (flattened as ecc-<name>) ---"

    $eccSubs = Get-ChildItem $eccSource -Directory -ErrorAction Stop
    foreach ($sub in $eccSubs) {
        $flatName = "ecc-$($sub.Name)"
        Sync-Entry `
            -LinkPath    (Join-Path $TargetRoot $flatName) `
            -TargetPath  $sub.FullName `
            -DisplayName $flatName
    }
} else {
    Write-Warn "ecc directory not found at $eccSource -- skipping ecc sub-skills"
}

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host " DRY RUN complete (no changes made)" -ForegroundColor Magenta
} else {
    Write-Host " Done" -ForegroundColor Cyan
}
Write-Host " Created : $($script:Created)"
Write-Host " Skipped : $($script:Skipped)  (already existed; use -Force to overwrite)"
Write-Host " Errors  : $($script:Errors)"
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($script:Errors -gt 0) { exit 1 }

