import abc
import logging
import random
from typing import Union, Optional
from datetime import datetime, timedelta

from ftdi_serial import NumberType

from .abc import IKADevice
from .errors import IKAError
from .utilities import _is_float_int

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ThermoshakerProtocol:
    """
    From the manual
    Command syntax and format:
        - commands and parameters are transmitted as capital letters
        - commands and parameters including successive parameters are seperated by at least one space (hex 0x20)
        - each individual command (including parameters and data and each response are terminated with
          Blank CR LF (hex 0x0d hex 0x0A) and have a maximum length of 80 characters
        - the decimal separator in a number is a dt (hex 0x2E)
    About watchdog:
        watchdog functions monitors the serial data flow. if, once this function has been activated there is no
        retransmission of the command from the computer within the set time ("watchog time:), the tempering and
        mixing functions are switched off in accordance with the set "watchdog" function or are changed to the set
        target values. data transmission may be interrupted by, for example, a crash in the operating system,
        a power failure in the pc, or an issue with the connection table between the computer and the device
        watchdog mode 1
            - if there is an interruption in data communications (longer than the set watchdog time), the tempering
            functions are switched off and Error 2 is displayed
        watchdog mode 2
            - if there is an interruption in data communications (longer than the set watchdog time), the temperature
            target value is changed to the WD safety temperature value. error message Error 2 is displayed
    """
    # thermoshaker NAMUR commands
    READ_ACTUAL_TEMPERATURE = "IN_PV_2"  # current actual temperature
    READ_ACTUAL_SPEED = "IN_PV_4"  # current actual shake speed
    READ_SET_TEMPERATURE = "IN_SP_2"  # temperature to go to
    READ_SET_SPEED = "IN_SP_4"  # speed to shake at
    SET_TEMPERATURE = "OUT_SP_2"  # set temperature to go to to xxx: OUT_SP_2 xxx
    SET_SPEED = "OUT_SP_4"  # set speed to shake at to xxx: OUT_SP_4 xxx
    # set the WD-safety temperature with echo of the set defined value: OUT_SP_12@n
    SET_WATCHDOG_SAFETY_TEMPERATURE = "OUT_SP_12@"
    # start the watchdog mode 1 and set the watchdog time to n (20 to 1500) second: OUT_WD1@N
    # echos the Watchdog time. during a WD1-event, the tempering functions are switched off. This command
    # needs to be sent within the watchdog time
    WATCHDOG_MODE_1 = "OUT_WD1@"
    # start the watchdog mode 2 and set the watchdog time to n (20 to 1500) second: OUT_WD2@N
    # echos the Watchdog time. during a WD2-event, the set temperature is changed to the WD safety temperature. This
    # command needs to be sent within the watchdog time
    WATCHDOG_MODE_2 = "OUT_WD2@"
    SWITCH_TO_NORMAL_OPERATING_MODE = 'RESET'
    START_TEMPERING = "START_2"
    STOP_TEMPERING = "STOP_2"
    START_MOTOR = "START_4"
    STOP_MOTOR = "STOP_4"
    READ_SOFTWARE_VERSION = 'IN_VERSION'
    READ_SOFTWARE_ID_AND_VERSION = 'IN_SOFTWARE_ID'


class AbstractThermoshaker(IKADevice):
    @abc.abstractmethod
    def __init__(self,
                 port: str,
                 dummy: bool = False,
                 ):
        """
        Abstract Driver for an IKA thermoshaker
        Supported/tested models:
            - MATRIX ORBITAL Delta Plus

        An abstract instance should not be instantiated. Instead use the create method or directly instantiate a
        Thermoshaker or DummyThermoshaker

        :param str, port: port to connect to the device
        :param bool, dummy: if dummy is true, then dont actually try to connect to the serial
            device (the thermomixer); used for testing without need to be connected to an actual thermomixer
        """
        IKADevice.__init__(
            self,
            port=port,
            dummy=dummy,
        )
        # track the last set watchdog safety temperature
        self._watchdog_safety_temperature: float = None

        if self.dummy:
            logger.debug('instantiated a DummyThermoshaker')
        else:
            logger.debug(f'connected to an IKA thermoshaker')

    @classmethod
    def create(cls,
               port: str,
               dummy: bool = False,
               ) -> Union['Thermoshaker', 'DummyThermoshaker']:
        """
        Constructs a hermoshaker or DummyThermoshaker the dummy flag in the kwargs. A Dummy instance does not
        communicate across a serial port and simulates actions and responses from a physical RealThermoshaker,

        :param str, port: port to connect to the device
        :param bool, dummy: if dummy is true, then dont actually try to connect to the serial
            device (the thermomixer); used for testing without need to be connected to an actual thermomixer
        :return: RealThermoshaker or DummyThermoshaker
        """
        target_class = DummyThermoshaker if dummy is True else Thermoshaker
        return target_class(port=port)

    @property
    def temperature(self) -> float:
        """actual temperature"""
        temp = self.request(ThermoshakerProtocol.READ_ACTUAL_TEMPERATURE)
        return temp

    @property
    def set_temperature(self) -> float:
        """the set temperature to go to"""
        temp = self.request(ThermoshakerProtocol.READ_SET_TEMPERATURE)
        return temp

    @set_temperature.setter
    def set_temperature(self, value: NumberType):
        if value is not None:
            if _is_float_int(value):
                logger.debug(f'set temperature to go to to {value}')
                self.request(f'{ThermoshakerProtocol.SET_TEMPERATURE} {value}')
            else:
                logger.error(f'unable to set temperature to go to {value}, value must be an int or float')
        else:
            logger.error(f'did not set temperature to go to; did not receive a value')

    @property
    def speed(self) -> float:
        """actual shake speed"""
        s = self.request(ThermoshakerProtocol.READ_ACTUAL_SPEED)
        return s

    @property
    def set_speed(self) -> float:
        """the set speed to shake at"""
        s = self.request(ThermoshakerProtocol.READ_SET_SPEED)
        return s

    @set_speed.setter
    def set_speed(self, value: NumberType):
        if value is not None:
            if _is_float_int(value):
                logger.debug(f'set speed to shake at to {value} rpm')
                self.request(f'{ThermoshakerProtocol.SET_SPEED} {value}')
            else:
                logger.error(f'unable to set speed to shake at to {value}, value must be an int or float')
        else:
            logger.error(f'did not set speed to shake at; did not receive a value')

    @property
    def watchdog_safety_temperature(self) -> Union[float, None]:
        """the watchdog safety temperature"""
        return self._watchdog_safety_temperature

    @watchdog_safety_temperature.setter
    def watchdog_safety_temperature(self, value: NumberType):
        if value is not None:
            if _is_float_int(value):
                logger.debug(f'set watchdog safety temperature to {value}')
                self.request(f'{ThermoshakerProtocol.SET_WATCHDOG_SAFETY_TEMPERATURE}{value}')
                self._watchdog_safety_temperature = value
            else:
                logger.error(f'unable to set the watchdog safety temperature to {value}, value must be an int or float')
        else:
            logger.error(f'did not set the watchdog safety temperature; did not receive a value')

    @property
    def software_version(self) -> str:
        sv = self.request(ThermoshakerProtocol.READ_SOFTWARE_VERSION)
        return sv

    @property
    def software_id_and_version(self) -> str:
        siv = self.request(ThermoshakerProtocol.READ_SOFTWARE_ID_AND_VERSION)
        return siv

    def start_tempering(self):
        logger.debug('start tempering')
        self.request(ThermoshakerProtocol.START_TEMPERING)

    def stop_tempering(self):
        logger.debug('stop tempering')
        self.request(ThermoshakerProtocol.STOP_TEMPERING)

    def start_shaking(self):
        logger.debug('start shaking')
        self.request(ThermoshakerProtocol.START_MOTOR)

    def stop_shaking(self):
        logger.debug('stop shaking')
        self.request(ThermoshakerProtocol.STOP_MOTOR)

    def start_watchdog_mode_1(self, t: int):
        """
        Start watchdog mode 1 and set the time or the watchdog to t seconds (20 - 1500)
        """
        if 20 <= t <= 1500:
            logger.debug(f'set watchdog mode 1 with watch time {t} seconds')
            self.request(f'{ThermoshakerProtocol.WATCHDOG_MODE_1}{t}')
        else:
            raise IKAError('watchdog mode time must be between 20 - 1500 seconds')

    def start_watchdog_mode_2(self, t: int):
        """
        Start watchdog mode 2 and set the time or the watchdog to t seconds (20 - 1500)
        """
        if 20 <= t <= 1500:
            logger.debug(f'set watchdog mode 2 with watch time {t} seconds')
            self.request(f'{ThermoshakerProtocol.WATCHDOG_MODE_2}{t}')
        else:
            raise IKAError('watchdog mode time must be between 20 - 1500 seconds')

    def switch_to_normal_operation_mode(self):
        """the concrete class should call this abstract method then continue with its implementation"""
        logger.debug('switch to normal operation mode')
        self.request(ThermoshakerProtocol.SWITCH_TO_NORMAL_OPERATING_MODE)

    def request(self,
                data: Union[bytes, str],
                timeout: Optional[NumberType] = None,
                line_ending: bytes = IKADevice.LINE_ENDING_ENCODED,
                ) -> Union[str, float]:
        """
        Perform a Serial request. Write data to the device and get a response back. The response is returned decoded
        as either a string or a float value.

        String response are for the ThermoshakerProtocols:
            - READ_SOFTWARE_VERSION
            - READ_SOFTWARE_ID_AND_VERSION
        Float response are for the ThermoshakerProtocols:
            - READ_ACTUAL_TEMPERATURE
            - READ_ACTUAL_SPEED
            - READ_SET_TEMPERATURE
            - READ_SET_SPEED
            - SET_WATCHDOG_SAFETY_TEMPERATURE

        :param data:
        :param timeout:
        :param line_ending:
        :return: a string or float, depending on the appropriate response based on the data
        """
        with self._lock:
            response: str = super().request(data, timeout, line_ending).decode()
            # the response except when asking for the software version or software version and id returns a number in
            # the format is '#.#.#' for software version and '#;#.#.#' for id and software version
            # the response when getting back a a float value is {serial command #.#}. except when setting the
            # watchdog safety temperature, that response is just a float value (#.#), and when starting watchdog mode
            # 1 or 2, that response is just an integer value
            # So first try to return the response as if the 1st index item after splitting the response by a white space
            # is a float, and if that doesnt work then return the response as if the 0th index item after splitting the
            # response by a white space is a float, and if that doesnt work then return the response as a string
            try:
                # try to get the 1st index as a float
                response: float = float(response.split()[1])
            except IndexError as e:
                # try to get the 0th index as a float
                try:
                    response: float = float(response.split()[0])
                except ValueError as e:
                    # response must be a string so just return the string
                    pass
        return response


class Thermoshaker(AbstractThermoshaker):
    def __init__(self,
                 port: str,
                 **kwargs,
                 ):
        """
        Driver for an IKA thermoshaker
        Supported/tested models:
            - MATRIX ORBITAL Delta Plus

        :param str, port: port to connect to the device
        :param Path, str, database_path: file path to the database to store data during operation
        :param str, component_name: name of the component, used for inserting records into the database and because
            the device subclasses ComponentState
        :param float, polling_frequency: polling frequency (s) for inserting entries into a the database
        """
        AbstractThermoshaker.__init__(self,
                                      port=port,
                                      dummy=False,
                                      )


class DummyThermoshaker(AbstractThermoshaker):
    DEFAULT_PORT = 'COM42'
    TEMPERATURE_FLUCTUATION: int = 1  # C
    SPEED_FLUCTUATION = 5  # rpm
    INITIAL_TEMPERATURE = 25.0
    INITIAL_SPEED = 0

    def __init__(self,
                 port: str = DEFAULT_PORT,
                 **kwargs,
                 ):
        """
        Dummy thermomoshaker for testing when not connected to a device
        """
        AbstractThermoshaker.__init__(self,
                                      port=port,
                                      dummy=True,
                                      )
        # track the last set temperature and speed
        self._set_temperature = self.INITIAL_TEMPERATURE  # C
        self._set_speed = self.INITIAL_SPEED  # rpm

        # used for providing dummy values for temperature and speed
        # the 'current' temperature;
        self._temperature = self.INITIAL_TEMPERATURE  # C
        # track whether tempering or not
        self._tempering = False
        # time it takes for the 'actual' (dummy) temperature to go from the current to the set temperature
        self.set_temperature_duration: timedelta = timedelta(minutes=10)
        # actual time that the 'actual' (dummy) temperature should be equal to the set temperature
        self.temperature_change_end_time: datetime = datetime.now()
        # the 'current' shake speed;
        self._speed = self.INITIAL_SPEED  # rpm
        # track whether shaking or not
        self._shaking = False
        # time it takes for the 'actual' (dummy) speed to go from the current to the set speed
        self.set_speed_duration: timedelta = timedelta(seconds=15)
        # actual time that the 'actual' (dummy) speed should be equal to the set speed
        self.speed_change_end_time: datetime = datetime.now()

    @property
    def temperature(self) -> float:
        """actual temperature"""
        now = datetime.now()
        if now >= self.temperature_change_end_time:
            # at or past the temperature end time
            if self._tempering is True:
                self._temperature = self._set_temperature
                return self._temperature
            else:
                # tempering stopped, so the temperature should decay to the initial value as time goes past the end
                # time. take the time to decay back to the initial stir rate as equal to the set_temperature_duration
                time_since_end = (now - self.temperature_change_end_time).seconds if (now - self.temperature_change_end_time).seconds is not 0 else 1
                # if time_since_end >= set_temperature_duration then the temperature_change_ratio is 1,
                # else the temperature_change_ratio is time_since_end/set_temperature_duration
                if time_since_end >= self.set_temperature_duration.seconds:
                    temperature_change_ratio = 1
                else:
                    temperature_change_ratio = time_since_end / self.set_temperature_duration.seconds
                temperature_change = temperature_change_ratio * (self._set_temperature - self.INITIAL_TEMPERATURE)  # C
                temperature_fluctuation = random.randrange(-self.TEMPERATURE_FLUCTUATION, self.TEMPERATURE_FLUCTUATION + 1)  # C
                temp = self._set_temperature - temperature_change + temperature_fluctuation
                return temp
        else:
            # still trying to reach the set temperature
            time_to_end = (self.temperature_change_end_time - now).seconds if (self.temperature_change_end_time - now).seconds is not 0 else 1
            total_temp_change = self._set_temperature - self._temperature  # C
            temp_change = total_temp_change * ((self.set_temperature_duration.seconds - time_to_end)/self.set_temperature_duration.seconds)  # C
            temp_fluctuation = random.randrange(-self.TEMPERATURE_FLUCTUATION, self.TEMPERATURE_FLUCTUATION + 1)  # C
            temp = self._temperature + temp_change + temp_fluctuation
            return temp

    @property
    def set_temperature(self) -> float:
        """the set temperature to go to"""
        return self._set_temperature

    @set_temperature.setter
    def set_temperature(self, value: NumberType):
        if value is not None:
            if _is_float_int(value):
                logger.debug(f'set temperature to go to to {value}')
                now = datetime.now()
                if now < self.temperature_change_end_time:
                    # did not reach the last set temperature, so update the stored current temperature before
                    # continuing
                    temp = self.temperature
                    self._temperature = temp
                    # add some more time to reach the new temperature end point
                    self.start_tempering()
                self._set_temperature = value
            else:
                logger.error(f'unable to set temperature to go to {value}, value must be an int or float')
        else:
            logger.error(f'did not set temperature to go to; did not receive a value')

    @property
    def speed(self) -> float:
        """actual shake speed"""
        now = datetime.now()
        if now >= self.speed_change_end_time:
            # at or past the speed end time
            if self._shaking is True:
                self._speed = self._set_speed
                return self._speed
            else:
                # shaking stopped, so the speed should decay to the initial value as time goes past the end time.
                # take the time to decay back to the initial stir rate as equal to the set_speed_duration
                time_since_end = (now - self.speed_change_end_time).seconds if (now - self.speed_change_end_time).seconds is not 0 else 1
                # if time_since_end >= set_speed_duration then the speed_change_ratio is 1,
                # else the speed_change_ratio is time_since_end/set_speed_duration
                if time_since_end >= self.set_speed_duration.seconds:
                    speed_change_ratio = 1
                else:
                    speed_change_ratio = time_since_end / self.set_speed_duration.seconds
                speed_change = speed_change_ratio * (self._set_speed - self.INITIAL_SPEED)  # rpm
                speed_fluctuation = random.randrange(-self.SPEED_FLUCTUATION, self.SPEED_FLUCTUATION + 1)  # rpm
                s = self._set_speed - speed_change + speed_fluctuation
                return s
        else:
            # still trying to reach the set speed
            time_to_end = (self.speed_change_end_time - now).seconds if (self.speed_change_end_time - now).seconds is not 0 else 1
            total_speed_change = self._set_speed - self._speed  # rpm
            speed_change = total_speed_change * ((self.set_speed_duration.seconds - time_to_end)/self.set_speed_duration.seconds)  # rpm
            speed_fluctuation = random.randrange(-self.SPEED_FLUCTUATION, self.SPEED_FLUCTUATION + 1)  # rpm
            s = self._speed + speed_change + speed_fluctuation
            return s

    @property
    def set_speed(self) -> float:
        """the set speed to shake at"""
        return self._set_speed

    @set_speed.setter
    def set_speed(self, value: NumberType):
        if value is not None:
            if _is_float_int(value):
                logger.debug(f'set speed to go to to {value}')
                now = datetime.now()
                if now < self.speed_change_end_time:
                    # did not reach the last set speed, so update the stored current speed before continuing
                    s = self.speed
                    self._speed = s
                    # add some more time to reach the new shake speed end point
                    self.start_shaking()
                self._set_speed = value
            else:
                logger.error(f'unable to set speed to go to {value}, value must be an int or float')
        else:
            logger.error(f'did not set speed to go to; did not receive a value')

    @Thermoshaker.watchdog_safety_temperature.setter
    def watchdog_safety_temperature(self, value: NumberType):
        if value is not None:
            if _is_float_int(value):
                logger.debug(f'set watchdog safety temperature to {value}')
                self._watchdog_safety_temperature = value
            else:
                logger.error(f'unable to set the watchdog safety temperature to {value}, value must be an int or float')
        else:
            logger.error(f'did not set the watchdog safety temperature; did not receive a value')

    @property
    def software_version(self) -> str:
        return "Dummy thermomshaker software version"

    @property
    def software_id_and_version(self) -> str:
        return "Dummy thermomshaker software id and version"

    def start_tempering(self):
        AbstractThermoshaker.start_tempering(self)
        self._tempering = True
        self.temperature_change_end_time = datetime.now() + self.set_temperature_duration

    def stop_tempering(self):
        AbstractThermoshaker.stop_tempering(self)
        self._tempering = False
        self._temperature = self.temperature
        self.temperature_change_end_time = datetime.now()

    def start_shaking(self):
        AbstractThermoshaker.start_shaking(self)
        self._shaking = True
        self.speed_change_end_time = datetime.now() + self.set_speed_duration

    def stop_shaking(self):
        AbstractThermoshaker.stop_shaking(self)
        self._shaking = False
        self._speed = self.speed
        self.speed_change_end_time = datetime.now()

    def request(self, data: Union[bytes, str], timeout: Optional[NumberType]=None, line_ending: bytes=b'\r'):
        return IKADevice.request(self, data, timeout, line_ending)

