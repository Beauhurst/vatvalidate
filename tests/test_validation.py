import pytest

from vatvalidate.validate import (
    _modulus_9755,
    get_digits_from_string,
    validate_with_9755_algorithm,
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
    ("vat_digits", "expected_validity"),
    [
        # Valid using the 97 algorithm
        ([7, 8, 7, 9, 7, 6, 2, 4, 2], True),
        ([9, 8, 5, 7, 8, 7, 3, 3, 9], True),
        ([5, 1, 0, 6, 1, 1, 4, 0, 5], True),
        ([7, 9, 3, 3, 7, 0, 6, 0, 2], True),
        ([5, 4, 4, 7, 8, 6, 2, 1, 3], True),
        ([7, 3, 6, 2, 9, 9, 5, 9, 5], True),
        ([1, 0, 9, 8, 5, 8, 6, 3, 6], True),
        ([5, 4, 1, 8, 9, 5, 2, 2, 5], True),
        ([9, 1, 0, 0, 8, 7, 0, 6, 2], True),
        ([8, 0, 0, 4, 6, 7, 7, 5, 1], True),
        # Invalid using the 97 algorithm
        ([3, 4, 4, 6, 4, 4, 7, 8, 8], False),
        ([2, 5, 8, 7, 6, 6, 6, 4, 8], False),
        ([2, 0, 8, 5, 9, 6, 0, 9, 3], False),
        ([2, 7, 5, 0, 1, 5, 0, 2, 5], False),
        ([3, 8, 6, 5, 5, 4, 4, 5, 5], False),
        ([4, 1, 4, 7, 1, 5, 4, 1, 4], False),
        ([1, 9, 6, 5, 6, 9, 7, 3, 9], False),
        ([3, 6, 0, 4, 0, 9, 3, 2, 0], False),
        ([3, 5, 6, 3, 9, 4, 6, 6, 6], False),
        ([4, 3, 7, 5, 5, 4, 5, 7, 4], False),
    ],
)
def test_modulus97(vat_digits: list[int], expected_validity: bool) -> None:
    assert _modulus_9755(vat_digits, use_9755=False) == expected_validity


@pytest.mark.parametrize(
    ("vat_digits", "expected_validity"),
    [
        # Valid using the 9755 algorithm
        ([3, 8, 8, 8, 3, 5, 5, 3, 1], True),
        ([2, 4, 4, 9, 8, 7, 6, 5, 8], True),
        ([2, 5, 2, 6, 3, 7, 6, 0, 1], True),
        ([2, 4, 9, 6, 3, 8, 3, 6, 6], True),
        ([2, 4, 6, 4, 0, 1, 8, 2, 0], True),
        ([2, 8, 1, 0, 0, 0, 4, 5, 3], True),
        ([3, 1, 9, 7, 6, 3, 8, 6, 7], True),
        ([2, 6, 2, 2, 6, 3, 4, 1, 8], True),
        ([1, 8, 7, 6, 4, 4, 8, 5, 6], True),
        ([2, 3, 1, 0, 9, 6, 5, 3, 2], True),
        # Invalid using the 9755 algorithm
        ([5, 0, 0, 2, 4, 8, 1, 0, 5], False),
        ([7, 0, 3, 2, 2, 6, 7, 7, 0], False),
        ([8, 0, 2, 1, 8, 1, 4, 7, 0], False),
        ([8, 5, 6, 6, 1, 4, 7, 9, 6], False),
        ([1, 0, 2, 8, 9, 0, 3, 9, 2], False),
        ([5, 6, 2, 9, 3, 7, 4, 1, 4], False),
        ([7, 5, 0, 2, 5, 5, 0, 5, 8], False),
        ([7, 3, 2, 3, 7, 0, 2, 5, 8], False),
        ([8, 5, 2, 2, 4, 3, 1, 4, 6], False),
        ([7, 9, 7, 3, 6, 4, 9, 6, 1], False),
    ],
)
def test_modulus9755(vat_digits: list[int], expected_validity: bool) -> None:
    assert _modulus_9755(vat_digits, use_9755=True) == expected_validity


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
    assert validate_with_9755_algorithm(vat_number) == expected_validity
