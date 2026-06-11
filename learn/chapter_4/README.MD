So, it this chapter we had a total guid how 
and why we might use aiohttp, what method it has 
and how to use it. 

The main advantage of aiohttp is that it's no-blocking 
IO library, witch we can use. 

It has great methods of operations with long-running
requests such as ```aiohttp.ClientTimeout(total=x, connect=y)```.
This method allows us to set a concrete timeout for request
like which will be in total, which only for connect. 


Also, in this chapter we had deep dive in creating tasks, 
learnt what ```gather```, ```as_completed``` and ```wait``` are
and what's the difference between them. 

More you could read in the code fils. 


# Summary 
<br>
We’ve learned how to use and create our own asynchronous context managers.
These are special classes that allow us to asynchronously acquire resources and
then release them, even if an exception occurred. These let us clean up any
resources we may have acquired in a non-verbose manner and are useful when
working with HTTP sessions as well as database connections. We can use them
with the special async with syntax.

 We can use the aiohttp library to make asynchronous web requests. aiohttp is a
web client and server that uses non-blocking sockets. With the web client, we
can execute multiple web requests concurrently in a way that does not block the
event loop.

 The asyncio.gather function lets us run multiple coroutines concurrently and
wait for them to complete. This function will return once all awaitables we pass
into it have completed. If we want to keep track of any errors that happen, we
can set return_exeptions to True. This will return the results of awaitables that
completed successfully alongside any exceptions we received.

 We can use the as_completed function to process results of a list of awaitables
as soon as they complete. This will give us an iterator of futures that we can loop
over. As soon as a coroutine or task has finished, we’ll be able to access the
result and process it.

 If we want to run multiple tasks concurrently but want to be able to understand
which tasks are done and which are still running, we can use wait. This function also allows us greater control on when it returns results. When it returns,
we get a set of tasks that have finished and set of tasks that are still running. We
can then cancel any tasks we wish or do any other awaiting we need.