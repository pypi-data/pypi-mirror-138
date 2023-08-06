# -*- coding: utf-8 -*-
# copyright 2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from typing import Dict, List, Set, Tuple, Optional, TypedDict
import re

from cubicweb.appobject import AppObject
from cubicweb.rset import ResultSet
from cubicweb_tsfacets import sqlcursor, convert_sql_to_rql, build_rset_descr


class FacetItemType(TypedDict):
    value: str
    count: str


class TSFacets(AppObject):
    """Base class for facets declaration.

    Each subclass of it allow to define a group of facets
    allowing to retrieve target entities. These entities don't have
    to be of the same type.

    Each subclass represent a specific postgresql table.

    :attr:`key_names_to_rql_definition`
        a dictionary linking each facet key with RQL returning a list of tuples:
        (entity eid to retrieve if selecting this facet, value of the facet)

    :attr:`text_search_indexation`
        a RQL request returning a list of tuples:
        (target entity eid, text to index for full text search)
    """

    __registry__ = "tsfacets"
    __abstract__ = True

    key_names_to_rql_definition: Dict[str, str] = {}

    text_search_indexation: str = ""

    target_etypes: Set = set()

    table_name: Optional[str] = None

    def _build_tsvector_parts(self, selected_facets: Dict[str, List[str]]):
        tsvector_parts = []
        for facet_key in self.key_names_to_rql_definition:
            values = selected_facets.get(facet_key)
            if not values:
                continue
            for value in values:
                tsvector_parts.append(f"{facet_key}.{value.lower()}")
        return tsvector_parts

    def _build_sql_parts(
        self,
        rql: str = None,
        rql_args: Dict = None,
        selected_facets: Dict[str, List[str]] = None,
        quote_to_use_in_sql="'",
    ) -> Tuple[str, str, Dict[str, str]]:
        ts_vector_parts = self._build_tsvector_parts(selected_facets or {})
        if ts_vector_parts:
            # here we use double ' because we will be inside a function.
            ts_vector_sql_part = f"""
                WHERE TSFT.facetvector @@ to_tsquery(
                    {quote_to_use_in_sql}{'&'.join(ts_vector_parts)}{quote_to_use_in_sql}
                )
            """
        else:
            ts_vector_sql_part = ""

        if rql:
            converted_sql, sql_args = convert_sql_to_rql(self._cw.cnx, rql, rql_args)
            sql_restriction_part = f"""
            JOIN ({converted_sql}) as _TABLE_FROM_RQL(target_eid)
            ON TSFT.eid = _TABLE_FROM_RQL.target_eid
            """
        else:
            sql_restriction_part = ""
            sql_args = {}
        if rql_args:
            sql_args.update(rql_args)

        return sql_restriction_part, ts_vector_sql_part, sql_args

    def get_facets_values_with_count(
        self,
        rql_restriction: str = None,
        rql_args: Dict = None,
        selected_facets: Dict[str, List[str]] = None,
    ) -> Dict[str, List[FacetItemType]]:
        """
        Retrieve all facet values with target entities count for each of them.
        :param rql_restriction: A RQL with a single variable in the Any close corresponding
        to the target entities.
        :param rql_args: arguments of rql_restriction.
        :param selected_facets: all selected facets as Dict[facet_key, [facet values]].
        :return: a dictionary of the type Dict[facet_key, Dict[value, target entity count]]
        """
        selected_facets = selected_facets or {}
        sql_restriction_part, ts_vector_sql_part, sql_args = self._build_sql_parts(
            rql_restriction, rql_args, selected_facets, quote_to_use_in_sql="''"
        )

        with sqlcursor(
            self._cw.cnx.repo,
            errmsg=(
                "Error with tsfacets table, are you sure "
                "you executed generate-tsfacets-tables ?"
            ),
        ) as crs:
            crs.execute(
                f"""
                SELECT
                    -- Break encoded words to get `code` and `value`
                    split_part(word, '.', 1) as code,
                    split_part(word, '.', 2) as value,
                    ndoc
                FROM
                    -- Word-count on all qualified records
                    ts_stat('
                        SELECT TSFT.facetvector
                        FROM {self.table_name} as TSFT
                        {sql_restriction_part}
                        {ts_vector_sql_part}
                    ')
                ORDER BY code, ndoc DESC;
                """,
                sql_args,
            )

            all_facets: Dict[str, List[FacetItemType]] = {}
            for code, value, count in crs.fetchall():
                if code not in self.key_names_to_rql_definition:
                    continue
                if value in selected_facets.get(code, []):
                    continue

                all_facets.setdefault(code, []).append(
                    {
                        "value": value,
                        "count": count,
                    }
                )

        return all_facets

    def get_target_entities_count(
        self,
        rql_restriction: str = None,
        rql_args: Dict = None,
        selected_facets: Dict[str, List[str]] = None,
    ) -> int:
        """
        Count target entities taking into account selected facets.
        :param rql_restriction: A RQL with a single variable in the Any close corresponding
        to the target entities.
        :param rql_args: arguments of rql_restriction.
        :param selected_facets: all selected facets as Dict[facet_key, [facet values]].
        :return: how many entities correspond to these facets.
        """
        sql_restriction_part, ts_vector_sql_part, sql_args = self._build_sql_parts(
            rql_restriction, rql_args, selected_facets
        )

        with sqlcursor(
            self._cw.cnx.repo,
            errmsg=(
                "Error with tsfacets table, are you sure "
                "you executed generate-tsfacet-tables ?"
            ),
        ) as crs:
            crs.execute(
                f"""
                SELECT COUNT(*)
                FROM {self.table_name} as TSFT
                {sql_restriction_part}
                {ts_vector_sql_part}
                """,
                sql_args,
            )
            try:
                return int(crs.fetchall()[0][0])
            except IndexError:
                return 0

    def get_target_entities_rset(
        self,
        base_rql: str,
        selected_facets: Dict[str, List[str]],
        rql_args: Dict = None,
    ) -> ResultSet:
        """
        Construct a rset corresponding to the selected facets.
        :param base_rql: a rql allowing to get target entities with all needed parameters.
        Target entity have to be the first variable in the Any clause.
        :param selected_facets: all selected facets as Dict[facet_key, [facet values]].
        :param rql_args: arguments for base_rql.
        :return: a CubicWeb ResultSet.
        """
        rql_args = rql_args or {}
        sql_restriction_part, ts_vector_sql_part, sql_args = self._build_sql_parts(
            base_rql, rql_args, selected_facets
        )
        limit_match = re.search(r"LIMIT \d+", sql_restriction_part)
        if limit_match:
            limit_part = limit_match.group(0)
            sql_restriction_part = sql_restriction_part.replace(limit_part, "")
        else:
            limit_part = ""
        offset_match = re.search(r"OFFSET \d+", sql_restriction_part)
        if offset_match:
            offset_part = offset_match.group(0)
            sql_restriction_part = sql_restriction_part.replace(offset_part, "")
        else:
            offset_part = ""

        with sqlcursor(
            self._cw.cnx.repo,
            errmsg=(
                "Error with tsfacets table, are you sure "
                "you executed generate-tsfacets-tables ?"
            ),
        ) as crs:
            crs.execute(
                f"""
                SELECT
                    _TABLE_FROM_RQL.*
                FROM
                    {self.table_name} as TSFT
                    {sql_restriction_part}
                {ts_vector_sql_part}
                {limit_part}
                {offset_part}
                """,
                {
                    **sql_args,
                    **rql_args,
                },
            )
            results = crs.fetchall()
        description = build_rset_descr(self._cw, base_rql, rql_args, results)
        rset = ResultSet(results, base_rql, rql_args, description)
        rset.req = self._cw
        return rset
