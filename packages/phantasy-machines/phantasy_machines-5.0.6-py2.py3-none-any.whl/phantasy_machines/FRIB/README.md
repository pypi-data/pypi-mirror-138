## Machine configuration for FRIB

* Machine Name: FRIB
* Included segments:
    - LEBT
    - MEBT
    - LS1_CA03
    - MEBT2DLine

How to use with ``phantasy``:

```python
from phantasy import MachinePortal

mp = MachinePortal(machine="FRIB", segment="LEBT")
```
