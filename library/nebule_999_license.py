"""
Nebule License Module
Equivalent to 999_license.php in PHP version

This module contains license information for the nebule library.
"""

NEBULE_LICENSE = """
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with this program.
If not, see https://www.gnu.org/licenses/.
"""

NEBULE_LICENSE_SHORT = "GNU GPL v3"
NEBULE_COPYRIGHT = "Copyright (C) 2010-2026 Project nebule"


def get_license():
    """Get the full license text."""
    return NEBULE_LICENSE


def get_license_short():
    """Get the short license name."""
    return NEBULE_LICENSE_SHORT


def get_copyright():
    """Get the copyright notice."""
    return NEBULE_COPYRIGHT
