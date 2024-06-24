# FastAPI-Cacher

FastAPI-Cacher is a caching library inspired by Flask-Caching, designed specifically for FastAPI. It provides an
easy-to-use decorator-based approach for adding caching to your FastAPI endpoints, making it simple and intuitive.

## Features

- Simple decorator-based caching similar to Flask-Caching.
- Support for various caching backends (Redis, Memcached, etc.).
- Easy integration with FastAPI applications.

## Installation

To install FastAPI-Cacher, use pip:

```bash
pip install fastapi-cacher
```

## Quick Start

Here's an example of how to use FastAPI-Cacher to cache an endpoint:

```python
from fastapi import FastAPI
from fastapi_cacher import FastAPICache, Cache

app = FastAPI()
cache = Cache(app)


@app.get('/')
@cache.cached(timeout=50)
async def index():
    return {'message': 'Hello, world!'}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Contributing

We welcome contributions! Please check the issues on GitHub and feel free to submit pull requests.

## License

This project is licensed under the MIT License.