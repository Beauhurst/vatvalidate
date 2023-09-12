def _modulus_9755(vat_digits: list[int], use_9755: bool = False) -> bool:
    """
    Applies the modulus 97 algorithm or the modulus 9755 algorithm to the provided
    vat digits.
    """
    # Multiply first seven digits by weights from 8 to 2 and sum them
    check_digits = 0
    for i in range(7):
        check_digits += vat_digits[i] * (8 - i)

    # Optionally add 55 (modulus 9755 algorithm)
    if use_9755:
        check_digits += 55

    # Subtract 97 until we get a negative number, then take the absolute value
    while check_digits > 0:
        check_digits -= 97
    check_digits = abs(check_digits)

    # convert summed digits to a list of ints
    check_digits = [int(char) for char in f"{abs(check_digits)}".zfill(2)]

    # Check calculated check_digits are the same as the last 2 given vat digits
    return check_digits == vat_digits[-2:]


def get_digits_from_string(vat_number: str) -> list[int]:
    """
    Returns a list of digits from a string, in the order they appear.
    """
    return [int(char) for char in vat_number if char.isdigit()]


def validate_with_9755_algorithm(vat_number: str) -> bool:
    """
    Runs the 97-55 algorithm for determining vat number validity on a vat number
    as described here: https://discover.hubpages.com/business/Check-VAT-Numbers-UK
    """
    vat_digits = get_digits_from_string(vat_number)

    # If there are not 9 digits then the vat number is not valid
    if len(vat_digits) != 9:
        return False

    # First: run the modulus 97 algorithm to check for validity
    if _modulus_9755(vat_digits, use_9755=False):
        return True

    # Second: if not valid with modulus 97, then run the modulus 9755 algorithm
    return _modulus_9755(vat_digits, use_9755=True)
