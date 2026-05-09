# Run this script in the d:\Projects\fastmovie directory to clean up the project.

# 1. Delete obvious temporary and cache files
Write-Host "Deleting __pycache__ and debug.txt..."
Remove-Item -Path "__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "debug.txt" -Force -ErrorAction SilentlyContinue

# 2. Create folders for uncertain/old files
Write-Host "Creating backup_files and old_scripts folders..."
New-Item -ItemType Directory -Force -Path "old_scripts" | Out-Null
New-Item -ItemType Directory -Force -Path "backup_files" | Out-Null

# 3. Move old or redundant scripts to old_scripts
Write-Host "Moving old scripts and redundant .bat files to old_scripts..."
$oldScripts = @(
    "INSTALL_LOGO.bat", 
    "RESTART_NOW.bat", 
    "RUN_SERVER.bat", 
    "START_SERVER.bat", 
    "install_logo.py", 
    "make_logo.py", 
    "test_email.py"
)

foreach ($file in $oldScripts) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "old_scripts" -Force
    }
}

# 4. Move a.html to backup_files
if (Test-Path "a.html") {
    Write-Host "Moving a.html to backup_files..."
    Move-Item -Path "a.html" -Destination "backup_files" -Force
}

# 5. Move launch.json to .vscode (or backup_files if it already exists there)
if (Test-Path "launch.json") {
    if (Test-Path ".vscode/launch.json") {
        Write-Host "Moving launch.json to backup_files (already exists in .vscode)..."
        Move-Item -Path "launch.json" -Destination "backup_files" -Force
    } else {
        Write-Host "Moving launch.json to .vscode..."
        Move-Item -Path "launch.json" -Destination ".vscode" -Force
    }
}

Write-Host "Cleanup complete!"
