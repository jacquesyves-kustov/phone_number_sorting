from random import randint
from typing import Final


class PhoneNumberGenerator:
    number_base: Final[str] = '+79'

    @classmethod
    def generate_random_numbers(cls, limit: int) -> list[str]:
        return [cls._generate_random_number() for _ in range(limit)]

    @classmethod
    def _generate_random_number(cls) -> str:
        new_number = cls.number_base

        for _ in range(9):
            new_number += str(randint(0, 9))

        return new_number
