from settings import cfg
from infra.controller import APIBuilder

apis = APIBuilder(cfg)
apis.build_stack()
app = apis.app


if __name__ == "__main__":
    import uvicorn

    app_base_configs = {
        "host": "0.0.0.0",
        "port": 8000,  # int(cfg.PORT),
        "workers": 1,  # int(cfg.UVICORN_WORKERS),
        "access_log": True,
        "reload": True,  # bool(cfg.RELOAD)
    }
    uvicorn.run("main:app", **app_base_configs)
