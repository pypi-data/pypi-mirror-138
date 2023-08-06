from airflow import AirflowException

try:
    from airflow.hooks.base import BaseHook

    HOOK_SOURCE = None
except ImportError:
    # For Airflow 1.10.*
    from airflow.hooks.base_hook import BaseHook

    HOOK_SOURCE = 'mcd_session'
from pycarlo.core import Session


class SessionHook(BaseHook):
    def __init__(self, mcd_session_conn_id: str):
        """
        MCD Session Hook. Retrieves connection details from connection extra.

        Expected format for extra -
        {
            "mcd_id": "foo",
            "mcd_token": "bar"
        }

        Note - the `mcd_token` can be a connection password instead (prioritized when present).

        :param mcd_session_conn_id: Connection ID for the MCD session.
        """
        self.mcd_session_conn_id = mcd_session_conn_id

        super().__init__(**(dict(source=HOOK_SOURCE) if HOOK_SOURCE is not None else {}))

    def get_conn(self) -> Session:
        """
        Gets a connection for the hook.

        :return: MCD access session.
        """
        connection = self.get_connection(self.mcd_session_conn_id)
        connection_extra = connection.extra_dejson
        try:
            return Session(
                mcd_id=connection_extra['mcd_id'],
                mcd_token=connection.password or connection_extra['mcd_token'],
                **(dict(endpoint=connection.host) if connection.host else {})
            )
        except KeyError as err:
            raise AirflowException(f'Missing expected key {err} from connection extra.')
