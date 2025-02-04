def camel_case_to_snake_case(s: str) -> str:
    """
    Convert a CamelCase string to snake_case.

    This function transforms a CamelCase string into snake_case. It also correctly handles
    abbreviations by ensuring that underscores are inserted only when an uppercase letter
    signals the beginning of a new word.

    For example:
      - If a lowercase letter precedes an uppercase letter, we insert an underscore.
      - If an uppercase letter is followed by a lowercase letter (indicating the start of a new word)
        even if it was preceded by an uppercase letter (as in abbreviations), we also insert an underscore.

    Examples:
        SomeSDK -> some_sdk
        RServoDrive -> r_servo_drive
        SDKDemo -> sdk_demo
    """
    result = []

    for i, char in enumerate(s):
        if char.isupper():
            # Check if an underscore is needed before this uppercase character.
            # Conditions for inserting an underscore:
            #   1. This is not the first character AND
            #   2. Either the previous character is lowercase (transitioning from a lower to uppercase)
            #      OR the next character exists and is lowercase (indicating the end of an abbreviation).
            if i > 0 and (s[i - 1].islower() or (i + 1 < len(s) and s[i + 1].islower())):
                result.append('_')
            result.append(char.lower())
        else:
            result.append(char)

    return ''.join(result)
