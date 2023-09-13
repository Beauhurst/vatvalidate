# vatvalidate

Ever wondered if that VAT number is valid? Well, now you can find out thanks to this simple Python library.

`vatvalidate` implements the modulus 97 and modulus 9755 used to check the validity of VAT numbers in the United Kingdom. For more info on these algorithms, see [this link](https://discover.hubpages.com/business/Check-VAT-Numbers-UK).

## Installation

To install `vatvalidate`, simply:

``` shell
$ pip install vatvalidate
```

## Usage

Using `validate_vat_number`, you can simply check the validity of vat number strings.
```python
from vatvalidate.validate import validate_vat_number

# Validate a vat number using validate_vat_number
vat_numbers = [
    "GB424807302",
    "424807302",
    "VAT NUMBER: 424807302",
    "GB279238956",
    "1234",
]

print(
    [validate_vat_number(number) for number in vat_numbers]
)
#> [True, True, True, False, False]
```
