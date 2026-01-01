"""Fixtures for MELCloud tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pymelcloud
import pytest

from homeassistant.components.melcloud.const import DOMAIN
from homeassistant.const import CONF_TOKEN, CONF_USERNAME

from tests.common import MockConfigEntry


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Create a mock MELCloud config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="test-email@test-domain.com",
        data={
            CONF_USERNAME: "test-email@test-domain.com",
            CONF_TOKEN: "test-token",
        },
        unique_id="test-email@test-domain.com",
    )


@pytest.fixture
def mock_ata_device() -> MagicMock:
    """Create a mock ATA (Air-to-Air) device."""
    device = MagicMock(spec=pymelcloud.AtaDevice)
    device.device_id = "ata123"
    device.building_id = "building123"
    device.name = "Test ATA Device"
    device.serial = "ATA123456"
    device.mac = "AA:BB:CC:DD:EE:FF"
    device.units = [{"model": "MSZ-LN25VG"}]
    device.room_temperature = 21.5
    device.target_temperature = 22.0
    device.target_temperature_min = 16.0
    device.target_temperature_max = 31.0
    device.temperature_increment = 0.5
    device.power = True
    device.operation_mode = pymelcloud.ata_device.OPERATION_MODE_HEAT
    device.operation_modes = [
        pymelcloud.ata_device.OPERATION_MODE_HEAT,
        pymelcloud.ata_device.OPERATION_MODE_COOL,
        pymelcloud.ata_device.OPERATION_MODE_DRY,
        pymelcloud.ata_device.OPERATION_MODE_FAN_ONLY,
    ]
    device.fan_speed = "auto"
    device.fan_speeds = ["auto", "low", "medium", "high"]
    device.vane_horizontal = "auto"
    device.vane_horizontal_positions = ["auto", "1", "2", "3", "4", "5", "swing"]
    device.vane_vertical = "auto"
    device.vane_vertical_positions = ["auto", "1", "2", "3", "4", "5", "swing"]
    device.has_energy_consumed_meter = True
    device.total_energy_consumed = 123.4
    device.has_outdoor_temperature = True
    device.outdoor_temperature = 5.0
    device.update = AsyncMock()
    device.set = AsyncMock()
    return device


@pytest.fixture
def mock_atw_device() -> MagicMock:
    """Create a mock ATW (Air-to-Water) device."""
    device = MagicMock(spec=pymelcloud.AtwDevice)
    device.device_id = "atw123"
    device.building_id = "building123"
    device.name = "Test ATW Device"
    device.serial = "ATW123456"
    device.mac = "11:22:33:44:55:66"
    device.units = [{"model": "ECODAN"}]
    device.temperature_increment = 0.5
    device.power = True
    device.status = pymelcloud.atw_device.STATUS_HEAT_ZONES
    device.operation_mode = "heat"
    device.operation_modes = ["heat", "cool"]
    device.outside_temperature = 8.0
    device.tank_temperature = 50.0
    device.target_tank_temperature = 55.0
    device.target_tank_temperature_min = 40.0
    device.target_tank_temperature_max = 60.0

    # Create a mock zone
    zone = MagicMock()
    zone.zone_index = 1
    zone.name = "Zone 1"
    zone.status = pymelcloud.atw_device.ZONE_STATUS_HEAT
    zone.room_temperature = 20.5
    zone.target_temperature = 21.0
    zone.flow_temperature = 35.0
    zone.return_temperature = 30.0
    zone.operation_mode = pymelcloud.atw_device.ZONE_STATUS_HEAT
    zone.set_target_temperature = AsyncMock()
    device.zones = [zone]

    device.update = AsyncMock()
    device.set = AsyncMock()
    return device


@pytest.fixture
def mock_get_devices(
    mock_ata_device: MagicMock, mock_atw_device: MagicMock
) -> Generator[MagicMock]:
    """Mock pymelcloud.get_devices."""
    with patch(
        "homeassistant.components.melcloud.coordinator.get_devices",
        return_value={
            pymelcloud.DEVICE_TYPE_ATA: [mock_ata_device],
            pymelcloud.DEVICE_TYPE_ATW: [mock_atw_device],
        },
    ) as mock:
        yield mock


@pytest.fixture
def mock_get_devices_empty() -> Generator[MagicMock]:
    """Mock pymelcloud.get_devices with empty result."""
    with patch(
        "homeassistant.components.melcloud.coordinator.get_devices",
        return_value={
            pymelcloud.DEVICE_TYPE_ATA: [],
            pymelcloud.DEVICE_TYPE_ATW: [],
        },
    ) as mock:
        yield mock


@pytest.fixture
def mock_login() -> Generator[MagicMock]:
    """Mock pymelcloud.login."""
    with patch(
        "homeassistant.components.melcloud.config_flow.pymelcloud.login",
        return_value="test-token",
    ) as mock:
        yield mock


@pytest.fixture
def mock_login_get_devices() -> Generator[MagicMock]:
    """Mock pymelcloud.get_devices in config_flow."""
    with patch(
        "homeassistant.components.melcloud.config_flow.pymelcloud.get_devices",
        return_value={
            pymelcloud.DEVICE_TYPE_ATA: [],
            pymelcloud.DEVICE_TYPE_ATW: [],
        },
    ) as mock:
        yield mock
