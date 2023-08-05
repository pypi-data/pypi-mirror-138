import sys


def run(main):
    """
      A very basic backport shim of the asyncio.run method from python 3.7
      so we have something that will work in python 3.6
      """
    if sys.version_info >= (3, 7):
        import asyncio
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        return asyncio.run(main, debug=True)
    else:
        from asyncio import events
        # events.get_event_loop() will throw an exception if there is no event loop running
        # so we have to use the "private" method here as that returns none. This is similar
        # to what asyncio.run does in 3.7 and above.
        if events._get_running_loop() is not None:
            loop = events.get_event_loop()
        else:
            loop = events.new_event_loop()
            events.set_event_loop(loop)
        return loop.run_until_complete(main)
