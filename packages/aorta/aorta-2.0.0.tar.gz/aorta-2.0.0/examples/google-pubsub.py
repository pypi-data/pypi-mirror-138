# pylint: skip-file
import asyncio

import unimatrix.runtime

import aorta


async def main():
    await unimatrix.runtime.startup()
    p = aorta.EventPublisher(
        transport=aorta.transport.GoogleTransport(
            project='unimatrixinfra',
            topic_path=lambda message: f'aorta.{message.kind}'
        )
    )
    futures = []
    for i in range(10):
        coro = p.publish({
            'apiVersion': 'v1',
            'kind': "FooEvent",
            'data': {'bar': 1, 'baz': 2, 'order': i}
        })
        futures.append(coro)
    await asyncio.gather(*futures)


if __name__ == '__main__':
    asyncio.run(main())
