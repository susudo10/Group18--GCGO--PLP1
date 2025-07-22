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
    def financial_status(self):
        if self.income_level < 50000 and self.dependents >= 3:
        return "High Need"
    elif self.income_level < 100000:
        return "Moderate Need"
    else:
        return "Low Need"

    @property
    def eligible_for_aid(self):
        """Gets the income level and number of dependents.
        If the income_level is less than 100 or dependents are >= 3."""
        return self.income_level < 100 or self.dependents >=3

    @property
    def update_info(self, name=None, contact=None, locality=None, income_level=None, dependents=None):
        """This allows for updates to the student's attributes.
        This is through using optional arguments allowing for updates on chosen fields only."""
        if name is not None:
            self.name = name
        if contact is not None:
            self.contact = contact
        if locality is not None:
            self.locality = locality
        if income_level is not None:
            self.income_level = income_level
        if dependents is not None:
            self.dependents = dependents
