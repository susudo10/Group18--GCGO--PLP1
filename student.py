#!/usr/bin/python3
"""
This module defines a Student class with student_id, name, date of birth,
contact, income_level, dependants, locality/region.
"""


class Student:
    """ Defines the class Student."""

    def __init__(self, student_id, name, contact, dob, school, income, dependents, region):
        """Initialises a new Student instance."""
        self.student_id = student_id
        self.name = name
        self.contact = contact
        self.dob = dob
        self.school = school
        self.income = income
        self.dependents = dependents
        self.region = region

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
    def update_info(self, name=None, contact=None, region=None, school=None, income=None, dependents=None):
        """
        Allows for updates to the student's attributes through using optional arguments allowing for updates on chosen fields only.
        """
        if name is not None:
            self.name = name
        if contact is not None:
            self.contact = contact
        if region is not None:
            self.region = region
        if income is not None:
            self.income = income
        if dependents is not None:
            self.dependents = dependents

def prompt_student_info():
    name = input("Enter student name: ")
    contact = input("Enter contact number: ")
    dob = input("Enter date of birth (YYYY-MM-DD): ")
    school = input("Enter the name of your school: ")
    income = float(input("Enter income level: "))
    dependents = int(input("Enter number of dependents: "))
    region = input("Enter region: ")
    school = input("Enter school name: ")

    # student_id can be None or assigned later
    return Student(None, name, contact, school, dob, income, dependents, region, school)
