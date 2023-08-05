

def create_tmp_byom_table(context, table: str = "ivsm_models_tmp"):
    context.execute(f"""
        CREATE VOLATILE TABLE {table}(
            model_version VARCHAR(255),
            model_id VARCHAR(255),
            model BLOB(2097088000)
        ) ON COMMIT PRESERVE ROWS;
        """)


def check_if_view_exists(context, database, name):
    rs = context.execute(f"""
    SELECT * FROM DBC.TABLES WHERE 
        TABLENAME ='{name}' AND 
        tablekind = 'V' AND 
        databasename='{database}'
    """)

    return rs.rowcount >= 1
