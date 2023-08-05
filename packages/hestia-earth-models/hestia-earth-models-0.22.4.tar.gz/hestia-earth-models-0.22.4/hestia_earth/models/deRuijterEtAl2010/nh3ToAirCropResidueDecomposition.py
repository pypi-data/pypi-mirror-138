from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition, TermTermType

from hestia_earth.models.log import debugRequirements, logRequirements, logShouldRun
from hestia_earth.models.utils.constant import Units, get_atomic_conversion
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.product import abg_residue_nitrogen, abg_total_residue_nitrogen_content
from hestia_earth.models.utils.dataCompleteness import _is_term_type_complete
from hestia_earth.models.utils.cycle import valid_site_type
from . import MODEL

TERM_ID = 'nh3ToAirCropResidueDecomposition'
TIER = EmissionMethodTier.TIER_1.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(residue_nitrogen_abg: float, nitrogenContent: float):
    A = min([
        max([(0.38 * 1000 * nitrogenContent/100 - 5.44), 0]) / 100,
        17 / 100
    ])
    debugRequirements(model=MODEL, term=TERM_ID,
                      A=A)
    value = A * residue_nitrogen_abg * get_atomic_conversion(Units.KG_NH3, Units.TO_N)
    return [_emission(value)]


def _should_run(cycle: dict):
    products = cycle.get('products', [])
    residue_nitrogen_abg = abg_residue_nitrogen(products)
    abg_residue_nitrogen_content = abg_total_residue_nitrogen_content(products)
    site_type_valid = valid_site_type(cycle)
    term_type_complete = _is_term_type_complete(cycle, {'termType': TermTermType.CROPRESIDUE.value})

    logRequirements(model=MODEL, term=TERM_ID,
                    residue_nitrogen=residue_nitrogen_abg,
                    abg_residue_nitrogen_content=abg_residue_nitrogen_content,
                    term_type_complete=term_type_complete,
                    site_type_valid=site_type_valid)

    should_run = all([
        site_type_valid,
        residue_nitrogen_abg > 0 or term_type_complete
    ])
    logShouldRun(MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, residue_nitrogen_abg, abg_residue_nitrogen_content


def run(cycle: dict):
    should_run, residue_nitrogen_abg, nitrogenContent = _should_run(cycle)
    return _run(residue_nitrogen_abg, nitrogenContent) if should_run else []
