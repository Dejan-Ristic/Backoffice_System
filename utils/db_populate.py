from app.models import Roles, Users
from flask import redirect


""" insert_roles() and superadmin() static methods (located in Roles and Users models) are used to ensure that
    all necessary roles for users and at least one user with superadmin permissions will be in the database.
"""

def db_populate():
    Roles.insert_roles()
    Users.superadmin()
    return redirect('/login')