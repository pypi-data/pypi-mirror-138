class RetryManager(object):
    """Context manager that counts attempts to run statements without
    exceptions being raised.
    - returns True when there should be more attempts
    """

    class _RetryProtector(object):
        """Context manager that only raises exceptions if its parent
        RetryManager has given up."""

        def __init__(self, retry_manager):
            self._retry_manager = retry_manager

        def __enter__(self):
            self._retry_manager._note_try()
            return self

        def __exit__(self, exc_type, exc_val, traceback):
            if exc_type is None:
                self._retry_manager._note_success()
            else:
                print(f"Exception: {exc_val}, will retry after sleep")
                pass

            # Suppress exception if the retry manager is still alive.
            return self._retry_manager.is_still_trying()

    def __init__(self, retries=1):

        self.max_retries = retries
        self.attempt_count = 0  # Note: 1-based.
        self._success = False

        self.protect = RetryManager._RetryProtector(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        print("Failed after multiple attempts")
        pass

    def _note_try(self):
        self.attempt_count += 1

    def _note_success(self):
        self._success = True

    def is_still_trying(self):
        return not self._success and self.attempt_count < self.max_retries

    def __bool__(self):
        return self.is_still_trying()


try:
    assert False
except Exception as e:
    print(f"ee {e}")


exit()

with RetryManager(retries=3) as rm:
    while rm:
        with rm.protect:
            print("Executing body")
            raise Exception("Some exception")

print("done")
