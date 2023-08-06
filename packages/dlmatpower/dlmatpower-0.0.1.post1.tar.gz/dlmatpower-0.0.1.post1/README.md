# dlmatpower

___

**ARCHIVED!!!** See [matpower-pip](https://github.com/yasirroni/matpower-pip) for better approach of using pypi.

___

Make download [MATPOWER](https://github.com/MATPOWER/matpower) easier from pip.

## Usage

### post-install (not supported by pip)

1. Clone this repository

2. Run "python setup.py install"

### pip (MATPOWER need to be downloaded after installation)

1. Install using `pip install dlmatpower`

2. Download MATPOWER using `dlmatpower.download()`

## Example

```python
import dlmatpower

dlmatpower.download()
```

## Note

Downloaded MATPOWER on `dlmatpower/` will not be removed by `pip uninstall dlmatpower`. Use `downloader.delete_default_download()` to remove it or manually delete downloaded content on `dlmatpower/`.
