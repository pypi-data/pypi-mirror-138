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


import os
import sys
import logging
import re

from collections import defaultdict
from collections import Counter

from fuzzywuzzy import fuzz

from gtdb_validation_tk.taxon_utils import is_latin_taxon, is_alphanumeric_taxon


class CheckTaxa(object):
    """Validation tests for taxon names."""

    def __init__(self, dpi=96):
        """Initialize."""

        self.logger = logging.getLogger()

    def check_for_typos(self, taxonomy):
        """Check for typos in taxon names.

        Iidentifies cases where root of child name is highly similar to,
        but not identical to root of parent name
        (e.g. f__Defferisomataceae; g__Deferrisoma -> missing 'f')
        """
        self.logger.info(
            'Identifying parent-child taxa with sufficiently similar, but non-identical names to suggest a typo.')
        rank_suffix = {1: 'ota', 2: 'ia',  3: 'ales', 4: 'aceae', 5: None}
        potential_issues = {}
        for gid, taxa in taxonomy.items():
            for rank_idx in range(1, 5):
                if rank_idx >= len(taxa):
                    # this violates the requirement of a 7-rank taxonomy,
                    # but this sort of issue will be picked up by other tests
                    continue

                # get parent name
                parent = taxa[rank_idx][3:]
                if '_' in parent:
                    parent = parent[0:parent.rfind('_')]

                if not parent.endswith(rank_suffix[rank_idx]):
                    continue

                parent_root = parent.replace(rank_suffix[rank_idx], '')

                # get child name
                child = taxa[rank_idx+1][3:]
                if '_' in child:
                    child = child[0:child.rfind('_')]

                if rank_suffix[rank_idx+1]:
                    if not child.endswith(rank_suffix[rank_idx+1]):
                        continue
                    child_root = child.replace(rank_suffix[rank_idx+1], '')
                else:
                    # genera have no fixed suffix
                    child_root = child

                # limit roots to shortest string as trailing characters
                # often mismatch
                # (e.g.  f__Streptomycetaceae -> Streptomycet;
                #        g__Streptomyces -> Streptomyces)
                min_root_len = min(len(parent_root), len(child_root))
                parent_root = parent_root[0:min_root_len]
                child_root = child_root[0:min_root_len]

                fuzzy_score = fuzz.ratio(parent_root, child_root)
                prefix_score = 0
                for idx in range(min_root_len):
                    if parent_root[idx] != child_root[idx]:
                        break

                    prefix_score += 1
                prefix_score = int(float(prefix_score)*100 / min_root_len)

                if (fuzzy_score != 100 and fuzzy_score >= 75
                        and prefix_score != 100 and prefix_score <= 50 and prefix_score != 0):
                    potential_issues['{}#{}'.format(parent, child)] = (
                        parent_root, child_root, fuzzy_score, prefix_score)

        print(
            ' - identified {:,} potential issues'.format(len(potential_issues)))
        if len(potential_issues) > 0:
            for conflict, tokens in potential_issues.items():
                parent, child = conflict.split('#')
                parent_root, child_root, fuzzy_score, prefix_score = tokens
                print(' - {} {}: fuzzy score = {}, prefix score = {}'.format(
                    parent,
                    child,
                    fuzzy_score,
                    prefix_score))

    def valid_taxon_name(self, taxonomy):
        """Check that taxon names have a valid form."""

        self.logger.info('Validating format of taxon names.')

        # get all Latin names
        latin_names = set()
        for taxa in taxonomy.values():
            for taxon in taxa:
                if is_latin_taxon(taxon):
                    latin_names.add(taxon)

        # check that placeholder names do not start
        # with full Latin name (e.g. Spirochaetae-1)
        invalid_latin_prefix = set()
        for taxa in taxonomy.values():
            for taxon in taxa:
                if taxon.startswith('s__'):
                    continue

                if is_alphanumeric_taxon(taxon):
                    m = re.search("[^a-z]", taxon[4:])
                    if m:
                        taxon_prefix = taxon[:m.start()+4]
                        if taxon_prefix in latin_names:
                            invalid_latin_prefix.add(taxon)

        if len(invalid_latin_prefix):
            print('')
            print('Placeholder name starts with a valid Latin name:')
            for taxon in invalid_latin_prefix:
                print('{}'.format(taxon))

        # check that names start with a capital letter
        invalid_capitalization = set()
        for taxa in taxonomy.values():
            for taxon in taxa:
                if len(taxon) > 3 and taxon[3].islower():
                    invalid_capitalization.add(taxon)

        if len(invalid_capitalization):
            print('')
            print('Taxa do not start with a capital letter:')
            for taxon in invalid_capitalization:
                print('{}'.format(taxon))
