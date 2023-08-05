# pylint: skip-file
import fastapi
import pydantic
import uvicorn

from aorta.transport.http import MessageReceiver


app = MessageReceiver(allowed_hosts=['*'])


if __name__ == '__main__':
    uvicorn.run('__main__:app',
        host="127.0.0.1",
        port=5000,
        log_level="debug",
        reload=True
    )
