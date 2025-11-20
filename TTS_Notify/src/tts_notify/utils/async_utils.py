"""
Async utilities for TTS Notify v2

This module provides async helper functions and utilities.
"""

import asyncio
import time
from typing import Any, Callable, Optional, List, Dict
import logging
from functools import wraps

logger = logging.getLogger(__name__)


class AsyncUtils:
    """Collection of async utility functions"""

    @staticmethod
    async def timeout_wrapper(coro, timeout: float):
        """
        Wrapper to add timeout to any coroutine.

        Args:
            coro: Coroutine to wrap
            timeout: Timeout in seconds

        Returns:
            Result of the coroutine or TimeoutError
        """
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"Operation timed out after {timeout} seconds")

    @staticmethod
    async def retry_wrapper(
        coro,
        max_retries: int = 3,
        delay: float = 1.0,
        backoff_factor: float = 2.0,
        exceptions: tuple = (Exception,)
    ):
        """
        Wrapper to add retry logic to any coroutine.

        Args:
            coro: Coroutine to wrap
            max_retries: Maximum number of retries
            delay: Initial delay between retries
            backoff_factor: Multiplier for delay on each retry
            exceptions: Exception types to retry on

        Returns:
            Result of the coroutine
        """
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                return await coro
            except exceptions as e:
                last_exception = e
                if attempt == max_retries:
                    logger.error(f"Failed after {max_retries} attempts: {e}")
                    raise

                wait_time = delay * (backoff_factor ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
                await asyncio.sleep(wait_time)

        # This should never be reached
        if last_exception:
            raise last_exception

    @staticmethod
    async def run_with_context(coro, context: Dict[str, Any]):
        """
        Run a coroutine with additional context.

        Args:
            coro: Coroutine to run
            context: Context dictionary

        Returns:
            Result of the coroutine
        """
        # Add context to coroutine's globals if needed
        # This is a simple implementation - could be enhanced
        return await coro

    @staticmethod
    async def gather_with_errors(*coros, return_exceptions: bool = False):
        """
        Gather multiple coroutines and collect results/errors.

        Args:
            *coros: Coroutines to gather
            return_exceptions: Whether to return exceptions instead of raising

        Returns:
            List of results or exceptions
        """
        results = []

        for coro in coros:
            try:
                result = await coro
                results.append(result)
            except Exception as e:
                if return_exceptions:
                    results.append(e)
                else:
                    logger.error(f"Error in coroutine: {e}")
                    raise

        return results

    @staticmethod
    async def batch_process(items: List[Any], processor: Callable, batch_size: int = 10):
        """
        Process items in batches.

        Args:
            items: Items to process
            processor: Async processing function
            batch_size: Size of each batch

        Yields:
            Batches of processed results
        """
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = await asyncio.gather(*[processor(item) for item in batch])
            yield batch_results

    @staticmethod
    async def race(*coros):
        """
        Run multiple coroutines and return the result of the first one to complete.

        Args:
            *coros: Coroutines to race

        Returns:
            Result of the first completed coroutine
        """
        try:
            done, pending = await asyncio.wait(
                [asyncio.create_task(coro) for coro in coros],
                return_when=asyncio.FIRST_COMPLETED
            )

            # Get result from first completed task
            for task in done:
                return task.result()

            # Cancel remaining tasks
            for task in pending:
                task.cancel()

        except Exception as e:
            # Cancel all tasks on error
            for task in asyncio.all_tasks():
                if not task.done():
                    task.cancel()
            raise

    @staticmethod
    def async_timer():
        """
        Context manager for timing async operations.

        Usage:
            async with AsyncUtils.async_timer() as timer:
                result = await some_async_function()
                print(f"Operation took {timer.duration:.2f}s")
        """
        return AsyncTimer()


class AsyncTimer:
    """Async timer context manager"""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.duration = None

    async def __aenter__(self):
        self.start_time = time.time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time


class AsyncTaskQueue:
    """Simple async task queue"""

    def __init__(self, max_workers: int = 5):
        self.queue = asyncio.Queue()
        self.workers = []
        self.max_workers = max_workers
        self.running = False

    async def _worker(self):
        """Worker coroutine"""
        while self.running:
            try:
                coro, future = await self.queue.get()
                if coro is None:  # Shutdown signal
                    break

                result = await coro
                future.set_result(result)

            except Exception as e:
                if not future.cancelled():
                    future.set_exception(e)

    async def start(self):
        """Start the worker pool"""
        self.running = True
        self.workers = [
            asyncio.create_task(self._worker())
            for _ in range(self.max_workers)
        ]

    async def stop(self):
        """Stop the worker pool"""
        self.running = False

        # Send shutdown signals
        for _ in range(self.max_workers):
            await self.queue.put((None, None))

        # Wait for workers to finish
        await asyncio.gather(*self.workers)

    async def submit(self, coro):
        """Submit a coroutine to be processed"""
        future = asyncio.Future()
        await self.queue.put((coro, future))
        return await future


def async_timed(func):
    """Decorator to time async functions"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"{func.__name__} completed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"{func.__name__} failed after {duration:.3f}s: {e}")
            raise

    return wrapper


def async_retry(max_retries: int = 3, delay: float = 1.0, backoff_factor: float = 2.0):
    """Decorator for async retry logic"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await AsyncUtils.retry_wrapper(
                func(*args, **kwargs),
                max_retries=max_retries,
                delay=delay,
                backoff_factor=backoff_factor
            )
        return wrapper
    return decorator


def async_timeout(timeout: float):
    """Decorator for async timeout logic"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await AsyncUtils.timeout_wrapper(
                func(*args, **kwargs),
                timeout=timeout
            )
        return wrapper
    return decorator


class AsyncRateLimiter:
    """Simple async rate limiter"""

    def __init__(self, max_calls: int, time_window: float):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []

    async def acquire(self):
        """Acquire permission to proceed"""
        now = time.time()

        # Remove old calls outside the time window
        self.calls = [call_time for call_time in self.calls if now - call_time < self.time_window]

        if len(self.calls) >= self.max_calls:
            # Calculate wait time until oldest call expires
            oldest_call = min(self.calls)
            wait_time = self.time_window - (now - oldest_call)
            if wait_time > 0:
                await asyncio.sleep(wait_time)

        self.calls.append(now)

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass