import logging
from dataclasses import dataclass
from enum import Enum
from typing import Tuple
_LOGGER = logging.getLogger("LupuTypes")


class DeviceClass(Enum):
    ALARM_STATE = "alarm_state"
    KEYPAD = "keypad"
    SIREN = "siren"
    SWITCH = "switch"
    UNKNOWN = "unkown"
    CONTACT = "contact",
    MOTION = "motion",
    SMOKE = "smoke",


class AlarmMode(Enum):
    DISARM = 0,
    ARM_AWAY = 1,
    ARM_NIGHT = 2,
    ARM_HOME = 3


@dataclass()
class SystemInfo():

    def __init__(self, version: str = "", rf_ver: str = "", zb_ver: str = "", zbs_ver: str = "", gsm_ver: str = "", publicip: str = "", ip: str = "",
                 mac: str = "", **kwargs):
        self.zbs_ver = zbs_ver
        self.gsm_ver = gsm_ver
        self.publicip = publicip
        self.ip = ip
        self.mac = mac
        self.zb_ver = zb_ver
        self.rf_ver = rf_ver
        self.version = version

    @property
    def unique_id(self):
        return self.mac.replace(":", "")


@dataclass()
class Battery():
    """
    Daten-Container, welcher den Zustand der Batterie widerspiegelt
    """

    __battery: str
    __battery_ok: bool

    def __init__(self, battery: str = "", battery_ok: int = -1, **kwargs):
        self.__battery = battery
        self.__battery_ok = bool(battery_ok)

    @property
    def is_ok(self) -> bool:
        return self.__battery_ok


@dataclass()
class Bypass():
    """
    Daten-Container, welcher den Zustand der zu ignorierende Sensormeldungen widerspiegelt
    """
    __bypass: bool
    __bypass_tamper: bool

    def __init__(self, bypass: int = -1, bypass_tamper: int = -1, **kwargs):
        self.__bypass = bool(bypass)
        self.__bypass_tamper = bool(bypass_tamper)

    @property
    def is_bypass_tamper(self) -> bool:
        return self.__bypass_tamper

    @property
    def is_bypass(self) -> bool:
        return self.__bypass


@dataclass()
class Tamper():
    """
    Daten-Container, welcher den Zustand des Sabotageschutzes eines Aktors widerspiegelt
    """
    __tamper: str
    __tamper_ok: bool

    def __init__(self, tamper: str = "", tamper_ok: int = -1, **kwargs):
        self.__tamper = tamper
        self.__tamper_ok = bool(tamper_ok)

    @property
    def is_ok(self) -> bool:
        return self.__tamper_ok


@dataclass()
class Location():
    """
    Daten-Container, welcher den Standort des Aktors widerspiegelt
    """
    __zone: int
    __area: int

    def __init__(self, area: int = -1, zone: int = -1, **kwargs):
        self.__zone = zone
        self.__area = area

    @property
    def area_zone(self) -> Tuple[int, int]:
        return self.__zone, self.__area


@dataclass()
class LupuDevice():
    _type: int
    _sid: str
    _name: str
    _battery: Battery
    _tamper: Tamper
    _location: Location
    _bypass: Bypass
    _alarm_status: str
    _rssi: int

    def __init__(self, type: int = -1, sid: str = "", name: str = "", alarm_status: str = "", rssi: int = -1, **kwargs):
        self._rssi = rssi
        self._type = type
        self._sid = sid
        self._name = name
        self._alarm_status = alarm_status
        self._battery = Battery(**kwargs)
        self._tamper = Tamper(**kwargs)
        self._location = Location(**kwargs)
        self._bypass = Bypass(**kwargs)

    @property
    def sid(self):
        return self._sid

    @property
    def is_alarm(self):
        return "BURGLAR" in self._alarm_status

    @property
    def battery(self) -> Battery:
        return self._battery

    @property
    def tamper(self) -> Tamper:
        return self._tamper

    @property
    def location(self) -> Location:
        return self._location

    @property
    def bypass(self) -> Bypass:
        return self._bypass

    @property
    def signal_strength(self) -> int:
        return self._rssi


# noinspection PyPep8Naming
@dataclass()
class ContactActor(LupuDevice):
    __open_close: bool

    def __init__(self, openClose: int = -1, **kwargs):
        super().__init__(**kwargs)
        self.__open_close = bool(openClose)

    @property
    def is_open(self):
        return self.__open_close


@dataclass()
class SwitchActor(LupuDevice):
    __on_off: int

    def __init__(self, onOff: int = -1, **kwargs):
        super().__init__(**kwargs)
        self.__on_off = bool(onOff)

    @property
    def is_on(self):
        return self.__on_off


@dataclass()
class MotionActor(LupuDevice):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def is_moving(self):
        return "DOORBELL" in self._alarm_status


@dataclass()
class SmokeActor(LupuDevice):
    __is_moving: bool

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def is_smoke_alarm(self):
        return "SMOKE" in self._alarm_status


@dataclass()
class AlarmPanel:
    __mode: AlarmMode
    __arm: bool

    def __init__(self, mode: AlarmMode = AlarmMode.DISARM, f_arm: int = -1):
        self.__mode = mode
        self.__arm = bool(f_arm)

    @property
    def arm_mode(self) -> Tuple[bool, AlarmMode]:
        return self.__arm, self.__mode

@dataclass()
class AlarmForm:
    __pcondform1: AlarmPanel
    __pcondform2: AlarmPanel
    __is_alarm: bool
    _battery: Battery
    _tamper: Tamper

    def __init__(self, updates: dict = {},forms:dict={},**kwargs):
        self.__pcondform1 = AlarmPanel(**forms["pcondform1"])
        self.__pcondform2 = AlarmPanel(**forms["pcondform2"])
        self.__battery = Battery(**updates)
        self.__tamper = Tamper(**updates)
        self.__is_alarm = bool(int(updates["alarm_ex"]))

    @property
    def area1_arm_mode(self) -> Tuple[bool, AlarmMode]:
        return self.__pcondform1.arm_mode

    @property
    def area2_arm_mode(self) -> Tuple[bool, AlarmMode]:
        return self.__pcondform2.arm_mode

    @property
    def battery(self) -> Battery:
        return self.__battery

    @property
    def tamper(self) -> Tamper:
        return self.__tamper

    @property
    def is_alarm(self) -> bool:
        return self.__is_alarm
