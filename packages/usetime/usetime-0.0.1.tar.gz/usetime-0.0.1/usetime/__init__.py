import time


class usetime:

    def timeClk(*args, **kwargs):
        def log_time(func):
            s1 = time.time()
            func()
            s2 = time.time()
            funtimes = s2-s1
            if len(args) != 0:
                if args[0] == "show":
                    print(funtimes)
            else:
                return funtimes
        return log_time
