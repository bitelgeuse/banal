<div align="center">
  <img src="assets/logo.png" alt="Banal logo" width="25%">
</div>

# Banal - 🎶 BPM Analyzer
Banal provides a web interface to analyze BPM.
* 📈 Chart of BPM dynamic.
* ⚙️ A lot of parameters of BPM distribution.
* 📝 Table of time intervals with BPM.

![Web Interface](./assets/interface.png)

## Requirements

* git
* python 3.12, 3.11 (other versions most likely work but are not tested)

## Installation

`setup.py` script create virtual environment and install python packages.
```shell
git clone https://github.com/bitelgeuse/banal.git
cd banal
python setup.py
```

## Usage

```shell
python run.py
```

## Remarks
* The first run may be a bit slow due to caching.
* The "Auto Correlation Window" parameter over 50 requires a LOT of RAM.
* The "Hop Length" parameter less 100 requires a LOT of RAM.

## Roadmap
* Create binaries
* Rewrite some parts of app to get more performance 
