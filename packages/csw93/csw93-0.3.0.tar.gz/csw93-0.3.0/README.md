# csw93
![PyPI](https://img.shields.io/pypi/v/csw93)

CSW93 is a Python package that generates all regular fractional factorial two-level designs from the 1993 paper of Chen, Sun and Wu: ["A catalogue of two-level and three-level fractional factorial designs with small runs"][1].

[1]: <https://www.jstor.org/stable/1403599>

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install csw93.

```bash
pip install csw93
```

## Usage

The pakage provides three function to get

- The design matrix,
- The word length pattern,
- The number of clear two-factor interactions,

using only the number of runs and the index of the design.
This index corresponds to the first column in all tables of all tables from the paper.

```python
import csw93

# Design matrix of the 16-run design with index 8-4.1
csw93.get_design(16, "8-4.1")

# Word length pattern of the 32-run design with index 15-10.2
csw93.get_wlp(32, "8-4.1")

# Number of clear two-factor interactions for the 64-run design 11-5.10
csw93.get_cfi(64, "11-5.10")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Changelog

- 0.2: corrected WLP's
- 0.1: initial version
