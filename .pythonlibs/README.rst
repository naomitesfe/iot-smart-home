Simple Asynchronous Scheduler
=============================

AsyncScheduler is a wrapper for sched.scheduler that provides
asynchronous operation out of the box. Thus, starting the scheduler does
not block the execution of the next statements. Further, adding and
removing events can be done without manually stopping/starting the
scheduler.

The event itself is executed synchronously. Consequently, it the
execution of the calling method takes longer than the delay to the next
event, execution of the next method is postponed until the previous
method returns.

Four different methods are available to add new events: \* ``enter`` -
adds a single event to take place in n seconds \* ``enterabs`` - adds a
single event to take place at time t \* ``repeat`` - adds a repeating
event that is triggered every n seconds \* ``enterabs`` - adds a
repeating event that is triggered at time t for the first time and then
every n seconds

Example
=======

Some events
-----------

Code
~~~~

::

    from asyncscheduler import AsyncScheduler
    from time import sleep

    a = AsyncScheduler()
    a.start()
    event = a.enter(1, 1, print, args=("event 1",))
    a.enter(2, 1, print, args=("event 2",))
    a.enter(3, 1, print, args=("event 3",))
    a.enter(4, 1, print, args=("event 4",))
    a.cancel(event)
    sleep(3.1)
    a.clear_scheduler()
    a.stop()

Output
~~~~~~

::

    event 2
    event 3

Digital clock
-------------

Code
~~~~

::

    from asyncscheduler import AsyncScheduler
    import time, datetime


    def display_time():
        print("\r{}".format(datetime.datetime.now().strftime("%H:%M:%S")), end='\r')


    a = AsyncScheduler()
    a.start()
    a.repeatabs(math.floor(time.time()) + 1, 1, 1, display_time)

    try:
        while True:
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass

    a.stop()

Output
~~~~~~

::

    12:34:56

API
===

enter
-----

``AsyncScheduler.enter(self, delay, priority, action, args=(), kwargs={})``

Add an event to the scheduler. It will be executed after the provided
delay with 'action(\*argument, \*\*kwargs)'. In case of two events
scheduled for the same time the priority is used for execution order. A
lower number means a higher priority.

Parameter: \* ``delay`` - delay call of func for this amount of seconds.
e.g. 12.34 \* ``priority`` - events scheduled for the same time are
processed according to their priority. \* ``action`` - function that is
called upon expires \* ``args`` - tuple of arguments for this function
\* ``kwargs`` - dict of arguments for this function

Returns the instance of the added event.

enterabs
--------

``AsyncScheduler.enterabs(self, time, priority, action, args=(), kwargs={})``

Add an event to the scheduler. It will be executed at the provided time
with 'action(\*argument, \*\*kwargs)'. In case of two events scheduled
for the same time the priority is used for execution order. A lower
number means a higher priority.

Parameter: \* ``time`` - call the action at this time stamp. \*
``priority`` - events scheduled for the same time are processed
according to their priority. \* ``action`` - function that is called
upon expires \* ``args`` - tuple of arguments for this function \*
``kwargs`` - dict of arguments for this function

Returns the instance of the added event.

clear\_scheduler
----------------

``AsyncScheduler.clear_scheduler(self)``

Cancels all scheduled events.

cancel
------

``AsyncScheduler.cancel(self, event)``

Remove the provided event from the scheduler. In case of an unknown
event, a ValueError will be raised.

Parameter: \* ``event`` - event instance as returned from add\_event.

repeat
------

``repeat(self, every, priority, action, args=(), kwargs={})``

Add a repeating event to the scheduler. It will be executed each time
the provided delay (every-n-seconds) has expired with 'func(\*argument,
\*\*kwargs)'. In case of two events scheduled for the same time the
priority is used for execution order. A lower number means a higher
priority.

See repeatabs for more information.

Parameter: \* ``time`` - call the action at this time stamp. \*
``every`` - every-n-seconds call action. e.g. 12.34 \* ``priority`` -
events scheduled for the same time are processed according to their
priority. \* ``action`` - function that is called upon expirey \*
``args`` - tuple of arguments for this function \* ``kwargs`` - dict of
arguments for this function

Returns the instance of the added event.

repeatabs
---------

``repeatabs(self, time, every, priority, action, args=(), kwargs={})``

Add a repeating event to the scheduler. It will be executed each time
the provided delay (every-n-seconds) has expired with 'func(\*argument,
\*\*kwargs)'. The first event is triggered at the provided time. In case
of two events scheduled for the same time the priority is used for
execution order. A lower number means a higher priority.

A repeating event will trigger one last time in case of a regular stop
with wait=False (=default).

Note: the returned event instance is the instance of the first iteration
only. Thus, after the first iteration it will not be part of
scheduler.queue no more. Instead a new event for this repeating event
has been created. AsyncScheduler keeps track of the current instance and
uses the first instance for identification of which event to cancel.
This is done with the method \_repeat\_event\_hash and the map
\_repeat\_event\_mapping.

Parameter: \* ``time`` - call the action at this time stamp. \*
``every`` - every-n-seconds call action. e.g. 12.34 \* ``priority`` -
events scheduled for the same time are processed according to their
priority. \* ``action`` - function that is called upon expirey \*
``args`` - tuple of arguments for this function \* ``kwargs`` - dict of
arguments for this function

Returns the instance of the added event.

start
-----

``start(self)``

Starts the scheduler.

stop
----

``stop(self)``

Stops the scheduler. After stop, the scheduler is emptied. Thus, calling
``start`` after ``stop`` results in a new, blank schedule that must be
filled.

Todos
=====

-  readthedocs
-  CI/CD

Misc
====

The code is written for ``python3`` (and tested with python 3.5).

`Merge
requests <https://gitlab.com/tgd1975/simple_asynchronous_scheduler/merge_requests>`__
/ `bug
reports <https://gitlab.com/tgd1975/simple_asynchronous_scheduler/issues>`__
are always welcome.

