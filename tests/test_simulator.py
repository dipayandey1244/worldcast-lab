import pandas as pd
import pytest
from worldcast.simulator import TransportWorld, Intervention


def test_simulator_is_reproducible():
    a = TransportWorld(cities=4, seed=11).run(steps=30)
    b = TransportWorld(cities=4, seed=11).run(steps=30)
    pd.testing.assert_frame_equal(a, b)


def test_simulator_shape_and_columns():
    frame = TransportWorld(cities=3, seed=2).run(steps=25)
    assert len(frame) == 75
    assert {"passenger_demand", "congestion", "revenue"}.issubset(frame.columns)


def test_intervention_changes_demand():
    base = TransportWorld(cities=3, seed=2).run(steps=30)
    treated = TransportWorld(cities=3, seed=2).run(
        steps=30, interventions=[Intervention(city=0, start=10, end=20, demand_multiplier=1.5)]
    )
    a = base.query("time >= 10 and time < 20 and city == 0").passenger_demand.mean()
    b = treated.query("time >= 10 and time < 20 and city == 0").passenger_demand.mean()
    assert b > a


def test_invalid_inputs():
    with pytest.raises(ValueError):
        TransportWorld(cities=1)
    with pytest.raises(ValueError):
        TransportWorld(cities=3).run(steps=10)
