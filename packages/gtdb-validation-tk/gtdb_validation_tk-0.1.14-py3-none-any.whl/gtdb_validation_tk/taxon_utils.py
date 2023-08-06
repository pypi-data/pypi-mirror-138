
###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################


def taxon_suffix(taxon):
    """Return alphabetic suffix of taxon."""

    if taxon[1:3] == '__':
        taxon = taxon[3:]

    if '_' in taxon:
        suffix = taxon.rsplit('_', 1)[1]
        return suffix

    return None


def is_placeholder_taxon(taxon):
    """Check if taxon name is a placeholder."""

    assert '__' in taxon  # expect taxon name to have rank prefix

    test_taxon = taxon[3:].replace('[', '').replace(']', '')
    if test_taxon == '':
        return True

    if any(c.isdigit() for c in test_taxon):
        return True

    if any(c.isupper() for c in test_taxon[1:]):
        return True

    return False


def is_latin_taxon(taxon):
    """Check iftaxon name is Latin."""

    return not is_placeholder_taxon(taxon)


def is_alphanumeric_taxon(taxon):
    """Check if taxon name is an alphanumeric placeholder.

    Example: g__9cdg1, f__UBA123, not not g__Prochlorococcus_A
    """

    return is_placeholder_taxon(taxon) and taxon_suffix(taxon) is None
