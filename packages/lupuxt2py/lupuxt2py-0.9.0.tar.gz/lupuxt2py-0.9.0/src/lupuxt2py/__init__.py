import asyncio
import logging
from typing import Dict, List

from .lupusec_service import LupusecSevice
from .lupusec_types import DeviceClass, LupuDevice, AlarmForm

_LOGGER = logging.getLogger("LupusecStateMachine")


class LupusecStateMachine:
    __devicesDict: Dict[DeviceClass, List[LupuDevice]] = dict()
    __panels: AlarmForm = None
    __is_polling: bool = False

    def __init__(self, ip_address, username, password, time):
        self.password = password
        self.username = username
        self.ip_address = ip_address
        self.__time = time
        self.__lupu_service = None

    def connect(self):
        self.__lupu_service = LupusecSevice(self.ip_address, self.username, self.password)

    def update(self):
        self.__refresh_devices()
        self.__refresh_panels()

    def poll(self):
        if self.__is_polling:
            return
        self.__is_polling = True
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__poll_devices())
        loop.run_until_complete(self.__poll_panels())

    def __refresh_devices(self):
        try:
            self.__devicesDict = self.__lupu_service.get_sensor_list()
        except Exception as ex:
            _LOGGER.error(ex)

    def __refresh_panels(self):
        try:
            self.__panels = self.__lupu_service.get_alarm_panel()
        except Exception as ex:
            _LOGGER.error(ex)

    async def __poll_devices(self):
        while True:
            await asyncio.sleep(self.__time)
            self.__refresh_devices()

    async def __poll_panels(self):
        while True:
            await asyncio.sleep(self.__time)
            self.__refresh_panels()

    @property
    def devices(self):
        return self.__devicesDict

    @property
    def panels(self):
        return self.__panels
