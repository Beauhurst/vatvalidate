from vatvalidate.exceptions import InvalidVATDigitsError


def _modulus_9755(
    weighted_digit_sum: int, vat_digits: list[int], use_9755: bool = False
) -> bool:
    """
    Checks the weighted_digit_sum of the first 7 digits of a VAT number against the
    last 2 digits of the VAT number to determine if the VAT number is valid, using
    either the modulus 97 algorithm or the modulus 9755 algorithm.
    """
    # Add 55 to the weighted digit sum if we are using the 9755 algorithm
    if use_9755:
        weighted_digit_sum += 55

    # Subtract 97 until we get zero or a negative number, then take the absolute
    # value. The outer modulo is what keeps an exact multiple of 97 at 0 instead of
    # wrapping it round to 97, so that numbers whose check digits are 00 validate.
    weighted_digit_sum = (97 - weighted_digit_sum % 97) % 97

    # convert zero-padded summed digits to a list of ints
    weighted_digit_sum_list: list[int] = [
        int(char) for char in f"{weighted_digit_sum:02n}"
    ]

    # Check calculated check_digits are the same as the last 2 given vat digits
    last_two_vat_digits: list[int] = vat_digits[-2:]
    return weighted_digit_sum_list == last_two_vat_digits


def get_digits_from_string(vat_number: str) -> list[int]:
    """
    Returns a list of digits from a string, in the order they appear.

    Non-digit characters are ignored. We test with `str.isdecimal()` rather than
    `str.isdigit()`, because `str.isdigit()` is also true for characters such as
    superscripts ("²") and circled digits ("①") that `int()` refuses to convert.
    """
    return [int(char) for char in vat_number if char.isdecimal()]


def sum_weighted_digits(vat_digits: list[int]) -> int:
    """
    Multiplies the first seven digits of the VAT number by weights from 8 to 2 & sums
    them to get a single integer against which we can compare the final two digits of a
    VAT number to check validity.
    """
    if len(vat_digits) != 9:
        raise InvalidVATDigitsError("VAT number must be 9 digits long.")

    check_digits: int = 0
    for i in range(7):
        check_digits += vat_digits[i] * (8 - i)
    return check_digits


def validate_vat_number(vat_number: str) -> bool:
    """
    Runs both the modulus 97 and the modulus 97-55 algorithm to determine if the given
    VAT number is valid.
    As described here: https://discover.hubpages.com/business/Check-VAT-Numbers-UK
    """
    vat_digits = get_digits_from_string(vat_number)

    # Get the weighted digit sum used by both the modulus 97 and 9755 algorithms
    try:
        weighted_digit_sum = sum_weighted_digits(vat_digits)
    except InvalidVATDigitsError:
        return False

    # First: run the modulus 97 algorithm to check for validity
    if _modulus_9755(
        weighted_digit_sum=weighted_digit_sum, vat_digits=vat_digits, use_9755=False
    ):
        return True

    # Second: if not valid with modulus 97, then run the modulus 9755 algorithm
    return _modulus_9755(
        weighted_digit_sum=weighted_digit_sum, vat_digits=vat_digits, use_9755=True
    )
