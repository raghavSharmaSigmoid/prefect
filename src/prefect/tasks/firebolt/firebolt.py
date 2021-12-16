import firebolt.db.connection as firebolt_conn

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs


class FireboltQuery(Task):
    def __init__(
        self,
        database: str = None,
        username: str = None,
        password: str = None,
        engine_name: str = None,
        query: str = None,
        **kwargs
    ):
        """
        Task for executing a query against a Firebolt database.

        Args:
            - database (str): name of the database to use
            - username (str): username used to authenticate
            - password (str): password used to authenticate
            - engine name (str): name of the engine to use
            - query (str): query to execute against database
            - **kwargs (dict, optional): additional keyword arguments to pass to the Task constructor
        """

        self.database = database
        self.username = username
        self.password = password
        self.engine_name = engine_name
        self.query = query
        super().__init__(**kwargs)

    @defaults_from_attrs("database", "username", "password", "engine_name", "query")
    def run(
        self,
        database: str = None,
        username: str = None,
        password: str = None,
        engine_name: str = None,
        query: str = None,
    ) -> list[list]:
        """
        Task run method. Executes a query against Firebolt database.

        Args:
            - database (str): name of the database to use
            - username (str): username used to authenticate
            - password (str): password used to authenticate
            - engine name (str): name of the engine to use
            - query (str): query to execute against database

        Returns:
            - List[List]: output of cursor.fetchall() if cursor.rowcount > 0 else an empty list

        Raises:
            - ValueError: if a required parameter is not supplied
            - DatabaseError: if exception occurs when executing the query
        """

        if not database:
            raise ValueError("A database name must be provided")
        if not username:
            raise ValueError("User name must be provided")
        if not password:
            raise ValueError("A password must be provided")
        if not engine_name:
            raise ValueError("An engine name must be provided")
        if not query:
            raise ValueError("A query string must be provided")

        conn_config = {
            "database": database,
            "username": username,
            "password": password,
            "engine_name": engine_name,
        }

        # connect to database, return a connection object
        conn = firebolt_conn.connect(**conn_config)
        result = []

        with conn:
            with conn.cursor() as cursor:
                execute = cursor.execute(query)
                if execute > 0:
                    result = cursor.fetchall()
        return result
