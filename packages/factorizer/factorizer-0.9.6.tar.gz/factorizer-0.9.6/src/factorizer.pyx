from libcpp.string cimport string
import requests
from requests.exceptions import Timeout as requestsTimeoutError
import threading
import time


class TimeOutError(Exception):
    pass



class BaseClass:

    def __init__(self, timeout=None):
        self.DETERMINISTIC = None
        if timeout is None or timeout<0:
            self.timeout = None
        else:
            self.timeout = timeout

        self.result = {}
        
    def factorize(self, n, *args, **kwargs):
        assert n>=0
        if n==0:
            return (0, 0)
        elif n==1:
            return (1, 1)
        assert self.DETERMINISTIC is not None
        args = (str(n).encode(),)+args
        thread_factorize = threading.Thread(target=self.factorize_wrap, args=args, kwargs=kwargs, name="_factorize", daemon=True)
        thread_factorize.start()
        if self.timeout is not None:
            for i in range(self.timeout*100):
                if thread_factorize.is_alive() == False:
                    break
                time.sleep(0.01)
            else:
                raise TimeOutError
        else:
            thread_factorize.join()


        d = self.result[str(n).encode()]
        d = int(d.decode())
        assert d*(n//d) == n
        return (d, n//d)

    
    def factorize_wrap(self, n, *args, **kwargs):
        d = self._factorize(n=n, args=args, kwargs=kwargs)
        self.result[n] = d

    
    def _factorize(self, string n, *args, **kwargs):
        return b"1"


class BruteForceFactorizer(BaseClass):

    def __init__(self, timeout=None):
        super().__init__(timeout)
        self.DETERMINISTIC = True

    def _factorize(self, string n, *args, **kwargs):
        cdef:
            string d
        with nogil:
            d = BruteForceFactorizer_cppfunc(n)
        return d


class FermatFactorizer(BaseClass):

    def __init__(self, timeout=None):
        super().__init__(timeout)
        self.DETERMINISTIC = True

    def _factorize(self, string n, *args, **kwargs):
        cdef:
            string d
        with nogil:
            d = FermatFactorizer_cppfunc(n)
        return d


class PollardsRhoFactorizer(BaseClass):

    def __init__(self, c=1, timeout=None):
        super().__init__(timeout)
        self.DETERMINISTIC = False
        self.c = c

    def _factorize(self, string n, *args, **kwargs):
        cdef:
            string d
            long c
        c = self.c
        with nogil:
            d = PollardsRhoFactorizer_cppfunc(n, c)
        return d


class RSAPrivateKeyFactorizer(BaseClass):

    def __init__(self, timeout=None):
        super().__init__(timeout)
        self.DETERMINISTIC = False

    def factorize(self, n, d, e=65537, *args, **kwargs):
        kwargs["d"] = d
        kwargs["e"] = e
        return super().factorize(n=n, args=args, kwargs=kwargs)

    def _factorize(self, string n, *args, **kwargs):
        cdef:
            string p, d, e
        d = str(kwargs["kwargs"]["kwargs"]["d"]).encode()
        e = str(kwargs["kwargs"]["kwargs"]["e"]).encode()
        with nogil:
            p = RSAPrivateKeyFactorizer_cppfunc(n, d, e)
        return p



class FactorDBFactorizer(BaseClass):
    
    def __init__(self, timeout=None):
        super().__init__(timeout)
        self.DETERMINISTIC = False
        self.ENDPOINT = "http://factordb.com/api"

    
    def _factorize(self, n):
        payload = {"query": n}
        
        try:
            r = requests.get(self.ENDPOINT, params=payload, timeout=self.timeout)
            return r.json()
        except requestsTimeoutError:
            raise TimeOutError
        except Exception as e:
            raise e

    def factorize(self, n, raw_result=False):
        if n==0:
            return (0, 0)
        elif n==1:
            return (1, 1)
        result = self._factorize(n)["factors"]
        if raw_result:
            return result
        
        if len(result)==1 and result[0][1]==1:
            return (1,n)
        else:
            d = int(result[0][0])
            assert d*(n//d) == n
            return (d, n//d)
        




