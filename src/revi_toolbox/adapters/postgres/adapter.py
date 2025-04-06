from typing import List, Union

import psycopg2
from psycopg2.extras import DictCursor
from pydantic import SecretStr

from revi_toolbox.adapters.postgres.schema import PostgreAuth


class PostgreAdapter:
    def __init__(
        self,
        username: str,
        password: SecretStr,
        hostname: str,
        port: int,
        db_name: str
    ):
        self.__auth_params = PostgreAuth(
            username = username,
            password = password,
            hostname = hostname,
            port = port,
            db_name = db_name
        )


    # Public
    def run_query(self, query: str, params: Union[dict, List[dict], None] = None) -> List[dict]:
        # Get Cursor
        conn = psycopg2.connect(self.__auth_params.uri.get_secret_value())
        cursor = conn.cursor(cursor_factory=DictCursor)

        # Run Query
        if (params is None): 
            cursor.execute(query)
        elif isinstance(params, List[dict]):
            cursor.executemany(query, params)
        else:
            cursor.execute(query, params)
        conn.commit()

        # Fetch Results (if exists)
        results = []
        try:
            results = [dict(r) for r in cursor.fetchall()]
        except psycopg2.ProgrammingError as exc:
            if str(exc).strip() != "no results to fetch":
                raise exc
        finally:
            conn.close()
        return results
