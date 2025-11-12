# Scale.py
A way to scale STL files without opening tinkercad lol

Author: Jack Hammerberg (jackmh)

Last Updated: 11/12/2025

This only works on Windows as far as I know
## Dependencies
1. Microsoft Visual C++ 14.0 or greater
```ps1
winget install Microsoft.VisualStudio.2022.BuildTools --override "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```
2. uv
```ps1
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
## Usage
```ps1
uv sync
uv run scale.py
```
## Building:
```ps1
pyinstaller --onefile scale.py
```