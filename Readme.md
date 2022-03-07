# Timebox

This library helps you backup your files or databases. It is based around a few core principles:
 
- input providers collect data
- transformers (not live yet) allow to transorm the collected data (compress, encode)
- output providers will store the data in the specified place
- rotation strategy will select which log files to delete


## Why another backup manager ?

I had a somewhat specific requirement, "decaying rotation" (more on that later), and none of the tools I found had exactly what I was looking for.

This project's name took inspiration from [blackbox](https://github.com/lemonsaurus/blackbox), another backup manager written in Python.

## Decaying rotation

The idea around decaying rotation is to keep a minimal number of backups, while keeping a long backup period. To do so, we have to keep some backups for a long time, while other will be short lived. This might be especially usefull when performing a backup of personal files, where you might realise you have deleted something usefull only a long time after the deletion has occured.

### Implementation

The method I found out was in fact the same as the [Tower of Hanoi roation scheme](https://en.wikipedia.org/wiki/Backup_rotation_scheme#Tower_of_Hanoi) (with some twists).

The specific implementation takes as input a `base`, which will determine the maximum time span of the backups: <img src="https://render.githubusercontent.com/render/math?math=2^{base + 1}">

Each <img src="https://render.githubusercontent.com/render/math?math=2^{base}"> days
![decaying backup](./notebooks/base3.png)
