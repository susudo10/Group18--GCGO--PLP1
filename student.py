#!/usr/bin/python3
"""
This module defines a Student class with student_id, name, date of birth,
contact, income_level, dependants, locality/region.
"""


class Student:
    """ Defines the class Student."""

    def __init__(self, id, name, contact, dob, income, dependents, region, school, amount_needed, priority_index):
        """Initialises a new Student instance."""
        self.id = id
        self.name = name
        self.contact = contact
        self.dob = dob
        self.income = income
        self.dependents = dependents
        self.region = region
        self.school = school
        self.amount_needed = amount_needed
        self.priority_index = priority_index


    @property
    def financial_status(self):
        """Returns a string indicating the financial need level."""
        if self.income < 50000 and self.dependents >= 3:
            return "High Need"
        elif self.income < 100000:
            return "Moderate Need"
        else:
            return "Low Need"

    @property
    def eligible_for_aid(self):
        """Determines aid eligibility based on income and dependents."""
        return self.income < 100000 or self.dependents >=3

    # Method to update to the student's attributes.
    def update_info(self, name=None, contact=None, dob=None, income=None, dependents=None, region=None, school=None):
        """
        Allows for updates to the student's attributes through using optional arguments allowing for updates on chosen fields only.
        """
        if name is not None:
            self.name = name
        if contact is not None:
            self.contact = contact
        if dob is not None:
            self.dob = dob
        if income is not None:
            self.income = income
        if dependents is not None:
            self.dependents = dependents
        if region is not None:
            self.region = region
        if school is not None:
            self.school = school
