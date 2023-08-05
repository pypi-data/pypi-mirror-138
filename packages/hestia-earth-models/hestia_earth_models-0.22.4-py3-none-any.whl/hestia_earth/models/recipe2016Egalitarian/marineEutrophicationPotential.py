from hestia_earth.schema import IndicatorStatsDefinition

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils import sum_values
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import convert_value_from_cycle, get_product, impact_value
from hestia_earth.models.utils.input import sum_input_impacts
from . import MODEL

TERM_ID = 'marineEutrophicationPotential'
LOOKUP_COLUMN = 'nEqEgalitarianMarineEutrophicationReCiPe2016'


def _indicator(value: float):
    indicator = _new_indicator(TERM_ID, MODEL)
    indicator['value'] = value
    indicator['statsDefinition'] = IndicatorStatsDefinition.MODELLED.value
    return indicator


def run(impact_assessment: dict):
    cycle = impact_assessment.get('cycle', {})
    product = get_product(impact_assessment)
    value = impact_value(TERM_ID, impact_assessment, LOOKUP_COLUMN)
    inputs_value = convert_value_from_cycle(product, sum_input_impacts(cycle.get('inputs', []), TERM_ID), None)
    logRequirements(model=MODEL, term=TERM_ID,
                    value=value,
                    inputs_value=inputs_value)
    logShouldRun(MODEL, TERM_ID, True)
    return _indicator(sum_values([value, inputs_value]))
