import pytest

from vatvalidate.exceptions import InvalidVATDigitsError
from vatvalidate.validate import (
    _modulus_9755,
    get_digits_from_string,
    sum_weighted_digits,
    validate_vat_number,
)


@pytest.mark.parametrize(
    ("vat_number", "expected_digits"),
    [
        ("GB252637601", [2, 5, 2, 6, 3, 7, 6, 0, 1]),
        ("GB249638366", [2, 4, 9, 6, 3, 8, 3, 6, 6]),
        ("GB246401820", [2, 4, 6, 4, 0, 1, 8, 2, 0]),
        ("GB 1630 403 49", [1, 6, 3, 0, 4, 0, 3, 4, 9]),
        ("GB 163 040 349", [1, 6, 3, 0, 4, 0, 3, 4, 9]),
        ("GB 16 3040 349", [1, 6, 3, 0, 4, 0, 3, 4, 9]),
        ("VAT NUMBER: 1630 403 49", [1, 6, 3, 0, 4, 0, 3, 4, 9]),
        ("GB262263418", [2, 6, 2, 2, 6, 3, 4, 1, 8]),
        ("GB1234 GB 5678-9", [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("🤗GB-1630😍403.49😂😂😂", [1, 6, 3, 0, 4, 0, 3, 4, 9]),
        ("GB/281/000-453", [2, 8, 1, 0, 0, 0, 4, 5, 3]),
        ("GB*31(976)38:67", [3, 1, 9, 7, 6, 3, 8, 6, 7]),
        ("GB2%6£2%26_3+418", [2, 6, 2, 2, 6, 3, 4, 1, 8]),
        ("1,8>7|644|!856", [1, 8, 7, 6, 4, 4, 8, 5, 6]),
        ("231096532 231096532", [2, 3, 1, 0, 9, 6, 5, 3, 2, 2, 3, 1, 0, 9, 6, 5, 3, 2]),
    ],
)
def test_get_digits_from_string(vat_number: str, expected_digits: list[int]) -> None:
    assert get_digits_from_string(vat_number) == expected_digits


@pytest.mark.parametrize(
    "vat_digits",
    [
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # too long
        ),
        ([1, 2, 8],),  # too short
    ],
)
def test_sum_weighted_digits_raises_value_error(vat_digits: list[int]) -> None:
    with pytest.raises(InvalidVATDigitsError):
        sum_weighted_digits(vat_digits)


@pytest.mark.parametrize(
    ("vat_digits", "expected_weighted_sum"),
    [
        ([2, 5, 2, 6, 3, 7, 6, 0, 1], 138),
        ([7, 8, 7, 9, 7, 6, 2, 4, 2], 249),
        ([9, 8, 5, 7, 8, 7, 3, 3, 9], 252),
        ([5, 1, 0, 6, 1, 1, 4, 0, 5], 92),
        ([7, 9, 3, 3, 7, 0, 6, 0, 2], 192),
        ([5, 4, 4, 7, 8, 6, 2, 1, 3], 181),
        ([7, 3, 6, 2, 9, 9, 5, 9, 5], 196),
        ([1, 0, 9, 8, 5, 8, 6, 3, 6], 158),
        ([5, 4, 1, 8, 9, 5, 2, 2, 5], 169),
        ([9, 1, 0, 0, 8, 7, 0, 6, 2], 132),
        ([8, 0, 0, 4, 6, 7, 7, 5, 1], 143),
        ([3, 4, 4, 6, 4, 4, 7, 8, 8], 148),
        ([2, 5, 8, 7, 6, 6, 6, 4, 8], 188),
        ([2, 0, 8, 5, 9, 6, 0, 9, 3], 143),
        ([2, 7, 5, 0, 1, 5, 0, 2, 5], 114),
        ([3, 8, 6, 5, 5, 4, 4, 5, 5], 181),
        ([4, 1, 4, 7, 1, 5, 4, 1, 4], 125),
        ([1, 9, 6, 5, 6, 9, 7, 3, 9], 197),
        ([3, 6, 0, 4, 0, 9, 3, 2, 0], 119),
        ([3, 5, 6, 3, 9, 4, 6, 6, 6], 170),
        ([4, 3, 7, 5, 5, 4, 5, 7, 4], 162),
    ],
)
def test_sum_weighted_digits(vat_digits: list[int], expected_weighted_sum: int) -> None:
    assert sum_weighted_digits(vat_digits) == expected_weighted_sum


@pytest.mark.parametrize(
    ("weighted_digit_sum", "vat_digits", "expected_validity"),
    [
        # Valid using the 97 algorithm
        (249, [7, 8, 7, 9, 7, 6, 2, 4, 2], True),
        (252, [9, 8, 5, 7, 8, 7, 3, 3, 9], True),
        (92, [5, 1, 0, 6, 1, 1, 4, 0, 5], True),
        (192, [7, 9, 3, 3, 7, 0, 6, 0, 2], True),
        (181, [5, 4, 4, 7, 8, 6, 2, 1, 3], True),
        (196, [7, 3, 6, 2, 9, 9, 5, 9, 5], True),
        (158, [1, 0, 9, 8, 5, 8, 6, 3, 6], True),
        (169, [5, 4, 1, 8, 9, 5, 2, 2, 5], True),
        (132, [9, 1, 0, 0, 8, 7, 0, 6, 2], True),
        (143, [8, 0, 0, 4, 6, 7, 7, 5, 1], True),
        # Invalid using the 97 algorithm
        (148, [3, 4, 4, 6, 4, 4, 7, 8, 8], False),
        (188, [2, 5, 8, 7, 6, 6, 6, 4, 8], False),
        (143, [2, 0, 8, 5, 9, 6, 0, 9, 3], False),
        (114, [2, 7, 5, 0, 1, 5, 0, 2, 5], False),
        (181, [3, 8, 6, 5, 5, 4, 4, 5, 5], False),
        (125, [4, 1, 4, 7, 1, 5, 4, 1, 4], False),
        (197, [1, 9, 6, 5, 6, 9, 7, 3, 9], False),
        (119, [3, 6, 0, 4, 0, 9, 3, 2, 0], False),
        (170, [3, 5, 6, 3, 9, 4, 6, 6, 6], False),
        (162, [4, 3, 7, 5, 5, 4, 5, 7, 4], False),
    ],
)
def test_modulus97(
    weighted_digit_sum: int, vat_digits: list[int], expected_validity: bool
) -> None:
    assert (
        _modulus_9755(
            weighted_digit_sum=weighted_digit_sum, vat_digits=vat_digits, use_9755=False
        )
        == expected_validity
    )


@pytest.mark.parametrize(
    ("weighted_digit_sum", "vat_digits", "expected_validity"),
    [
        # Valid using the 9755 algorithm
        (205, [3, 8, 8, 8, 3, 5, 5, 3, 1], True),
        (178, [2, 4, 4, 9, 8, 7, 6, 5, 8], True),
        (138, [2, 5, 2, 6, 3, 7, 6, 0, 1], True),
        (170, [2, 4, 9, 6, 3, 8, 3, 6, 6], True),
        (119, [2, 4, 6, 4, 0, 1, 8, 2, 0], True),
        (86, [2, 8, 1, 0, 0, 0, 4, 5, 3], True),
        (169, [3, 1, 9, 7, 6, 3, 8, 6, 7], True),
        (121, [2, 6, 2, 2, 6, 3, 4, 1, 8], True),
        (180, [1, 8, 7, 6, 4, 4, 8, 5, 6], True),
        (107, [2, 3, 1, 0, 9, 6, 5, 3, 2], True),
        # Invalid using the 9755 algorithm
        (92, [5, 0, 0, 2, 4, 8, 1, 0, 5], False),
        (124, [7, 0, 3, 2, 2, 6, 7, 7, 0], False),
        (124, [8, 0, 2, 1, 8, 1, 4, 7, 0], False),
        (195, [8, 5, 6, 6, 1, 4, 7, 9, 6], False),
        (102, [1, 0, 2, 8, 9, 0, 3, 9, 2], False),
        (180, [5, 6, 2, 9, 3, 7, 4, 1, 4], False),
        (136, [7, 5, 0, 2, 5, 5, 0, 5, 8], False),
        (136, [7, 3, 2, 3, 7, 0, 2, 5, 8], False),
        (148, [8, 5, 2, 2, 4, 3, 1, 4, 6], False),
        (230, [7, 9, 7, 3, 6, 4, 9, 6, 1], False),
    ],
)
def test_modulus9755(
    weighted_digit_sum: int, vat_digits: list[int], expected_validity: bool
) -> None:
    assert (
        _modulus_9755(
            weighted_digit_sum=weighted_digit_sum, vat_digits=vat_digits, use_9755=True
        )
        == expected_validity
    )


@pytest.mark.parametrize(
    ("vat_number", "expected_validity"),
    [
        # Valid VAT numbers
        ("GB830927231", True),
        ("GB504073485", True),
        ("GB843361042", True),
        ("GB286173282", True),
        ("GB367209637", True),
        ("GB938453395", True),
        ("GB317778860", True),
        ("GB277363669", True),
        ("GB813058943", True),
        ("GB716043854", True),
        ("GB162137682", True),
        ("GB133158337", True),
        ("GB945698169", True),
        ("GB212690920", True),
        ("GB424807302", True),
        # Invalid VAT numbers (fails on 97 and 97-55)
        ("GB741850801", False),
        ("GB971286211", False),
        ("GB849680863", False),
        ("GB274560225", False),
        ("GB800451425", False),
        ("GB206404539", False),
        ("GB128932508", False),
        ("GB279238956", False),
        ("GB123456789", False),
        ("GB333102445", False),
        ("GB847188421", False),
        ("GB862795875", False),
        ("GB137354608", False),
        ("GB834204846", False),
        ("GB268959823", False),
        # Invalid VAT numbers (too long)
        ("GB2834204846", False),
        ("GB27368959823", False),
        ("800451425000", False),
        ("GB 1373 005 46 08", False),
        ("GB849680863000", False),
        # Invalid VAT numbers (too short)
        ("GB15827200", False),
        ("GB1783052", False),
        ("GB941737", False),
        ("Not a VAT Number", False),
        ("000 111", False),
        (" ", False),
    ],
)
def test_valid_vat_numbers(vat_number: str, expected_validity: bool) -> None:
    assert validate_vat_number(vat_number) == expected_validity
