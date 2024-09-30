import pytest
from freezegun import freeze_time

from resty.application.rest_timer.services import FullHalfHourCalculator


@pytest.fixture(scope='function')
def service():
    return FullHalfHourCalculator()


@freeze_time('28.07.2024 15:18')
def test__calculate_full_half_hour_time_sec__before_30(
    service: FullHalfHourCalculator
):
    expected = 12 * 60    # 12 минут переводим в секунды

    assert service.calculate_full_half_hour_time_sec() == expected


@freeze_time('28.07.2024 15:35')
def test__calculate_full_half_hour_time_sec__after_30(
    service: FullHalfHourCalculator
):
    expected = 25 * 60    # 25 минут переводим в секунды
    assert service.calculate_full_half_hour_time_sec() == expected


@freeze_time('28.07.2024 15:30')
def test__calculate_full_half_hour_time_sec__exactly_30(
    service: FullHalfHourCalculator
):
    expected = 30 * 60    # 30 минут переводим в секунды
    assert service.calculate_full_half_hour_time_sec() == expected


@freeze_time('28.07.2024 15:00')
def test__calculate_full_half_hour_time_sec__exactly_00(
    service: FullHalfHourCalculator
):
    expected = 30 * 60    # 30 минут переводим в секунды
    assert service.calculate_full_half_hour_time_sec() == expected
