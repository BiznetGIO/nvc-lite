import pytest
from app import create_app, celery
import asyncio
import threading
import time
from celery.signals import worker_ready
from app.helpers import asyncio_helper
WORKER_READY = list()

@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture(scope='function')
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        loop.close()

@pytest.fixture(scope='function')
def test_asyncio_helper():
    data = asyncio_helper._invoke_requests

class Worker(threading.Thread):
    """Run the Celery worker in a background thread."""

    def run(self):
        """Run the thread."""
        celery_args = ['-C', '-q', '-c', '1', '-P', 'solo', '--without-gossip']
        with create_app().app_context():
            celery.worker_main(celery_args)


@worker_ready.connect
def on_worker_ready(**_):
    """Called when the Celery worker thread is ready to do work.
    This is to avoid race conditions since everything is in one python process.
    """
    WORKER_READY.append(True)


@pytest.fixture(autouse=True, scope='session')
def celery_worker():
    """Start the Celery worker in a background thread."""
    thread = Worker()
    thread.daemon = True
    thread.start()
    for i in range(10):  # Wait for worker to finish initializing to avoid a race condition I've been experiencing.
        if WORKER_READY:
            break
        time.sleep(1)