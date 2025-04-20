import re
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
        elif isinstance(params, list):
            __query = self.__reparse_query_many(cursor, query, params)
            cursor.execute(__query)
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


    # Private
    def __reparse_query_many(self, cursor: DictCursor, query: str, params: List[dict]) -> str:
        values_params = re.findall(r"(?<=VALUES )[^;\n]+", query)
        __query = query
        if (values_params):
            value_inj = ", ".join(
                cursor.mogrify(values_params[0], p).decode("utf-8")
                for p in params
            )
            __query = re.sub(r"(?<=VALUES )[^;\n]+", value_inj, query)
        return __query
