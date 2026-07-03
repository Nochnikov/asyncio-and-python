from multiprocessing import Pool

def say_hello(name: str) -> str:
    return f'Hello, {name}!'


if __name__ == '__main__':
    with Pool() as process_pool:
        """
        This method looks similar to what we did previously with the
        Process class, where we passed in a target function and a tuple of arguments. 
        The difference here is that we don’t need to start the process or call join on it ourselves. 
        We also get back the return value of our function, which we couldn’t do in the previous
        example
        """
        """Sync one"""
        # hi_nurdaulet = process_pool.apply(say_hello, args=('Nurdaulet',))
        # hi_indira = process_pool.apply(say_hello, args=('Indira',))
        # print(hi_nurdaulet)
        # print(hi_indira)

        # Async One
        hi_nurdaulet = process_pool.apply_async(say_hello, args=('Nurdaulet',))
        hi_indira = process_pool.apply_async(say_hello, args=('Indira',))
        """Even though the process now running 
        concurrently, the main process is still will be 
        blocked here. The .get() method."""
        print(hi_nurdaulet.get())
        print(hi_indira.get())
