from cubicweb_tsfacets import convert_sql_to_rql, sqlcursor


def build_facet_table(cnx, facet_cls):
    table_name = facet_cls.table_name
    with sqlcursor(cnx.repo, errmsg=f"could not build {table_name} table.") as crs:
        target_etype_sql_part = ",".join(
            (f"'{etype}'" for etype in facet_cls.target_etypes)
        )
        crs.execute(
            f"""
            CREATE TEMPORARY TABLE {table_name}_entities AS (
                SELECT eid FROM entities WHERE type IN ({target_etype_sql_part})
            )
        """
        )
        from_parts = []
        vector_parts = []
        args = {}
        for facet_key, rql in facet_cls.key_names_to_rql_definition.items():
            sql, _args = convert_sql_to_rql(cnx, rql)
            args.update(_args)
            from_parts.append(
                f"""
            LEFT OUTER JOIN ({sql}) as _f{facet_key}(target_eid,value)
            ON entities.eid = _f{facet_key}.target_eid
            """
            )
            vector_parts.append(
                f"""
                ARRAY_AGG(
                    DISTINCT CASE WHEN _f{facet_key}.value is NULL
                    THEN ''  ELSE '{facet_key}.' || _f{facet_key}.value END
                )
                """
            )
        if facet_cls.text_search_indexation:
            sql, _args = convert_sql_to_rql(cnx, facet_cls.text_search_indexation)
            args.update(_args)
            fti_vector_from = f"""
            LEFT OUTER JOIN ({sql}) as _tstable(target_eid, text)
            ON entities.eid = _tstable.target_eid
            """
            fti_vector = "TO_TSVECTOR(_tstable.text) as textsearchvector"
        else:
            fti_vector = "NULL as textsearchvector"
            fti_vector_from = ""
        crs.execute(f"DROP TABLE IF EXISTS {table_name}")
        crs.execute(
            f"""
                CREATE TABLE {table_name} AS (
                    SELECT
                        entities.eid,
                        ARRAY_TO_TSVECTOR(
                            ARRAY_REMOVE(
                                {"||".join(vector_parts)},
                                ''
                            )
                        ) as facetvector,
                        {fti_vector}
                    FROM
                        {table_name}_entities AS entities
                        {" ".join(from_parts)}
                        {fti_vector_from}
                    GROUP BY entities.eid
                    {", _tstable.text" if fti_vector else ""}
                )
            """,
            args,
        )
        crs.execute(
            f"CREATE INDEX {table_name}_ginidx ON {table_name} USING GIN(textsearchvector)"
        )
        crs.execute(
            f"CREATE INDEX {table_name}_fti_ginidx ON {table_name} USING GIN(facetvector)"
        )
