import threading

from saorm14 import exc
from saorm14.testing import async_test
from saorm14.testing import eq_
from saorm14.testing import expect_raises
from saorm14.testing import expect_raises_message
from saorm14.testing import fixtures
from saorm14.testing import is_true
from saorm14.util import asyncio
from saorm14.util import await_fallback
from saorm14.util import await_only
from saorm14.util import greenlet_spawn
from saorm14.util import queue

try:
    from greenlet import greenlet
except ImportError:
    greenlet = None


async def run1():
    return 1


async def run2():
    return 2


def go(*fns):
    return sum(await_only(fn()) for fn in fns)


class TestAsyncioCompat(fixtures.TestBase):
    __requires__ = ("greenlet",)

    @async_test
    async def test_ok(self):

        eq_(await greenlet_spawn(go, run1, run2), 3)

    @async_test
    async def test_async_error(self):
        async def err():
            raise ValueError("an error")

        with expect_raises_message(ValueError, "an error"):
            await greenlet_spawn(go, run1, err)

    @async_test
    async def test_propagate_cancelled(self):
        """test #6652"""
        cleanup = []

        async def async_meth_raise():
            raise asyncio.CancelledError()

        def sync_meth():
            try:
                await_only(async_meth_raise())
            except:
                cleanup.append(True)
                raise

        async def run_w_cancel():
            await greenlet_spawn(sync_meth)

        with expect_raises(asyncio.CancelledError, check_context=False):
            await run_w_cancel()

        assert cleanup

    @async_test
    async def test_sync_error(self):
        def go():
            await_only(run1())
            raise ValueError("sync error")

        with expect_raises_message(ValueError, "sync error"):
            await greenlet_spawn(go)

    def test_await_fallback_no_greenlet(self):
        to_await = run1()
        await_fallback(to_await)

    @async_test
    async def test_await_only_no_greenlet(self):
        to_await = run1()
        with expect_raises_message(
            exc.MissingGreenlet,
            r"greenlet_spawn has not been called; can't call await_\(\) here.",
        ):
            await_only(to_await)

        # ensure no warning
        await greenlet_spawn(await_fallback, to_await)

    @async_test
    async def test_await_fallback_error(self):
        to_await = run1()

        await to_await

        async def inner_await():
            nonlocal to_await
            to_await = run1()
            await_fallback(to_await)

        def go():
            await_fallback(inner_await())

        with expect_raises_message(
            exc.MissingGreenlet,
            "greenlet_spawn has not been called and asyncio event loop",
        ):
            await greenlet_spawn(go)

        await to_await

    @async_test
    async def test_await_only_error(self):
        to_await = run1()

        await to_await

        async def inner_await():
            nonlocal to_await
            to_await = run1()
            await_only(to_await)

        def go():
            await_only(inner_await())

        with expect_raises_message(
            exc.InvalidRequestError,
            r"greenlet_spawn has not been called; can't call await_\(\) here.",
        ):
            await greenlet_spawn(go)

        await to_await

    @async_test
    async def test_contextvars(self):
        import asyncio
        import contextvars

        var = contextvars.ContextVar("var")
        concurrency = 5

        async def async_inner(val):
            eq_(val, var.get())
            return var.get()

        def inner(val):
            retval = await_only(async_inner(val))
            eq_(val, var.get())
            eq_(retval, val)
            return retval

        async def task(val):
            var.set(val)
            return await greenlet_spawn(inner, val)

        values = {
            await coro
            for coro in asyncio.as_completed(
                [task(i) for i in range(concurrency)]
            )
        }
        eq_(values, set(range(concurrency)))

    @async_test
    async def test_require_await(self):
        def run():
            return 1 + 1

        assert (await greenlet_spawn(run)) == 2

        with expect_raises_message(
            exc.AwaitRequired,
            "The current operation required an async execution but none was",
        ):
            await greenlet_spawn(run, _require_await=True)


class TestAsyncAdaptedQueue(fixtures.TestBase):
    __requires__ = ("greenlet",)

    def test_lazy_init(self):
        run = [False]

        def thread_go(q):
            def go():
                q.get(timeout=0.1)

            with expect_raises(queue.Empty):
                asyncio.run(greenlet_spawn(go))
            run[0] = True

        t = threading.Thread(
            target=thread_go, args=[queue.AsyncAdaptedQueue()]
        )
        t.start()
        t.join()

        is_true(run[0])

    @async_test
    async def test_error_other_loop(self):
        run = [False]

        def thread_go(q):
            def go():
                eq_(q.get(block=False), 1)
                q.get(timeout=0.1)

            with expect_raises_message(
                RuntimeError, ".* to a different .*loop"
            ):
                asyncio.run(greenlet_spawn(go))

            run[0] = True

        q = queue.AsyncAdaptedQueue()

        def prime():
            with expect_raises(queue.Empty):
                q.get(timeout=0.1)

        await greenlet_spawn(prime)
        q.put_nowait(1)
        t = threading.Thread(target=thread_go, args=[q])
        t.start()
        t.join()

        is_true(run[0])
