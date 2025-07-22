#!/usr/bin/python3
"""
This module defines a Student class with student_id, name, date of birth,
contact, income_level, dependants, locality/region
"""


class Student:
    """ Defines the class Student."""

    def __init__(self, student_id, name, contact, dob, income_level, dependents, region):
        """Initialised a new Student instance."""
        self.name = name
        self.contact = contact
        self.dob = dob
        self.income_level = income_level
        self.dependents = dependents
        self.income_level = income_level
        self.depedents = dependents
        self.region = region

    @property
    def eligible_for_aid(self):
        """Gets the income level and number of dependents.
        If the income_level is less than 100 or dependents are >= 3."""
        return self.income_level < 100 or self.dependents >=3
