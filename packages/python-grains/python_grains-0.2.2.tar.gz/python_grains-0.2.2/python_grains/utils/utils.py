import redis
from functools import partial
import random
import time
from redis.commands.core import CoreCommands

class RedisClientWithRetry(object):

    methods = (c for c in dir(CoreCommands) + ['pipeline',
                                               'get_connection_kwargs']
               if not c.startswith('_'))

    def __init__(self, redis_client, max_retry=5):
        assert max_retry > 0, 'max_retry should be larger than zero'
        self.redis_client = redis_client
        self.max_retry = max_retry
        self.attach_methods()

    @classmethod
    def from_config(cls, *args, max_retry=5, **kwargs):
        redis_client = redis.StrictRedis(*args, **kwargs)
        return cls(redis_client=redis_client, max_retry=max_retry)

    def attach_methods(self):
        for method in self.methods:
            if not hasattr(self, method):
                setattr(self, method, partial(self._run_method, method))

    def _run_method(self, method, *args, **kwargs):
        n_retry = 0
        while n_retry <= self.max_retry:
            try:
                return getattr(self.redis_client, method)(*args, **kwargs)
            except redis.exceptions.ConnectionError as e:
                error = e
                backoff = 3.0 ** n_retry / 10
                n_retry += 1
                time.sleep(backoff + random.random() / 10)
        raise error

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))