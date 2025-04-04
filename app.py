# app.py
from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from oks_routes import oks_router
from dependencies import provide_session

openapi_config = OpenAPIConfig(title="KSI OKS API", version="1.0.0")

app = Litestar(
    route_handlers=[oks_router],
    dependencies={"db_session": provide_session},
    openapi_config=openapi_config
)