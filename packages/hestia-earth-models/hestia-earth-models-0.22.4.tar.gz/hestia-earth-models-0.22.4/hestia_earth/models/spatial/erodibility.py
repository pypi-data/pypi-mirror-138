from hestia_earth.schema import MeasurementStatsDefinition

from hestia_earth.models.log import logShouldRun
from hestia_earth.models.utils.measurement import _new_measurement
from .utils import download, find_existing_measurement, has_geospatial_data, _site_gadm_id
from . import MODEL

TERM_ID = 'erodibility'
EE_PARAMS = {
    'collection': 'erodibility',
    'type': 'raster',
    'reducer': 'mean'
}
BIBLIO_TITLE = 'Modelling spatially explicit impacts from phosphorus emissions in agriculture'


def _measurement(value: float):
    measurement = _new_measurement(TERM_ID, MODEL, BIBLIO_TITLE)
    measurement['value'] = [value]
    measurement['statsDefinition'] = MeasurementStatsDefinition.SPATIAL.value
    return measurement


def _download(site: dict):
    return download(
        collection=EE_PARAMS['collection'],
        ee_type=EE_PARAMS['type'],
        reducer=EE_PARAMS['reducer'],
        fields=EE_PARAMS['reducer'],
        latitude=site.get('latitude'),
        longitude=site.get('longitude'),
        gadm_id=_site_gadm_id(site),
        boundary=site.get('boundary')
    ).get(EE_PARAMS['reducer'])


def _run(site: dict):
    value = find_existing_measurement(TERM_ID, site) or _download(site)
    return [_measurement(value)] if value else []


def _should_run(site: dict):
    should_run = has_geospatial_data(site)
    logShouldRun(MODEL, TERM_ID, should_run)
    return should_run


def run(site: dict): return _run(site) if _should_run(site) else []
