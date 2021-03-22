from django.db import models
from fuzzywuzzy import fuzz


class Person(models.Model):
    """Data Structure for representing a Person."""

    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    birth_date = models.DateField(blank=True, null=True, default=None)
    bsn = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        managed = False

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def match(self, other) -> int:
        """Calculate the probability that two persons are the same.

        Matching logic:
            If the BSN number matches then 100%
            Otherwise:
                * If the last name is the same +40%
                * If the first name is the same +20%
                * If the first name is similar +15% (see examples)
                * If the date of birth matches + 40%
                * If the dates of birth are known and not the same, there is no match

        Args:
            other: other person to compare

        Returns:
            Probability that that matched persons are the same
        """
        # If the BSN number matches then 100% (else 0%!)
        if self.bsn and other.bsn:
            if self.bsn == other.bsn:
                return 100
            return 0

        # If the dates of birth are known ... AND not the same, there is no match
        if self.birth_date and other.birth_date:
            if self.birth_date != other.birth_date:
                return 0

        result = 0

        # If the last name is the same +40%
        if self.last_name and other.last_name:
            if self.last_name == other.last_name:
                result += 40

        # If the first name is the same +20%
        if self.first_name and other.first_name:
            if self.first_name == other.first_name:
                result += 20

            # If the first name is similar +15% (see examples)
            elif fuzz.ratio(self.first_name, other.first_name) > 90:
                result += 15

        # If the dates of birth are known ... AND If the date of birth matches + 40%
        if self.birth_date and other.birth_date:
            if self.birth_date == other.birth_date:
                result += 40

        return result
