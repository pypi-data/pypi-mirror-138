from pkgutil import extend_path
from enum import Enum
from hestia_earth.utils.tools import current_time_ms

from .log import logger
from .gee_utils import init_gee
from .boundary import run as run_boundary
from .coordinates import run as run_coordinates
from .gadm import run as run_gadm

__path__ = extend_path(__path__, __name__)


class RunType(Enum):
    BOUNDARY = 'boundary'
    COORDINATES = 'coordinates'
    GADM = 'gadm'


RUN_BY_TYPE = {
    RunType.BOUNDARY.value: lambda v: run_boundary(v),
    RunType.COORDINATES.value: lambda v: run_coordinates(v),
    RunType.GADM.value: lambda v: run_gadm(v)
}


def _unsupported_type(type, *args): raise Exception(f"Unsupported type: {type}")


def run(run_type: RunType, data: dict):
    init_gee()

    now = current_time_ms()
    run_type_s = run_type if isinstance(run_type, str) else run_type.value
    result = RUN_BY_TYPE.get(run_type_s, _unsupported_type)(data)
    logger.info('time=%s, unit=ms', current_time_ms() - now)
    return result
