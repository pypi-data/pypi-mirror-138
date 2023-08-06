import logging
from base64 import b64encode

from graypy import GELFHTTPHandler
import urllib3


class GELFHTTPSBasicAuthHandler(GELFHTTPHandler):
    def __init__(self,
                 host: str,
                 username: str,
                 password: str,
                 port=443,
                 compress=True,
                 path="/gelf",
                 timeout=5,
                 conn_pool_max_sz=1,
                 block=False,
                 retries=None,
                 **kwargs):
        super().__init__(host=host, port=port, compress=compress, path=path, timeout=timeout, **kwargs)
        auth = b64encode(f'{username}:{password}'.encode()).decode("ascii")
        self.headers['Authorization'] = f'Basic {auth}'
        self.headers['Connection'] = 'Keep-Alive'
        self.headers['Content-Type'] = 'application/json'
        # Use pool for thread safety and to graceful reuse connections
        self._pool = urllib3.HTTPSConnectionPool(
            host=host,
            port=port,
            timeout=timeout,
            maxsize=conn_pool_max_sz,
            retries=retries or urllib3.Retry(total=1),
            block=block,
        )
        self._is_emitting = False

    def __del__(self):
        self._pool.close()

    def emit(self, record: logging.LogRecord):
        if self._is_emitting:
            # Protect from recursive logs while emitting log record
            return

        pickle = self.makePickle(record)
        try:
            self._is_emitting = True
            resp = self._pool.request('POST', self.path, body=pickle, headers=self.headers)
            resp.release_conn()
        except urllib3.exceptions.HTTPError:
            log = logging.getLogger(__name__)
            log.exception('Failed to send record')
        finally:
            self._is_emitting = False
