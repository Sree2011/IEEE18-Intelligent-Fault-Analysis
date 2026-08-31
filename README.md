# IEEE 18-Bus Intelligent Fault Analysis

Python-only reimplementation of the user's original MATLAB/Octave project.

## Stage 1
- Bus/line/generator data
- Y-bus construction
- Newton-Raphson load flow
- Basic validation/tests

> Note: the original repository's data tables and solver documentation use inconsistent
> column definitions. This Python version uses the *actual row layout* in `busdata.m`
> and exposes generator metadata separately so the model is explicit rather than silently
> interpreting columns incorrectly.

## Environment

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run:

```powershell
python -m power_system.main
```

Run tests:

```powershell
python -m pytest
```
