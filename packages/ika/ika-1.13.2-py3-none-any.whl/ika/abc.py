import logging
from typing import Union, Optional
from abc import ABC, abstractmethod
import threading

from ftdi_serial import Serial, NumberType
from hein_control.states.component import ComponentState

from .errors import IKAError


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class IKADevice(Serial, ComponentState, ABC):
    # default connection parameters for an IKA device
    CONNECTION_SETTINGS = dict(
        baudrate=9600,
        data_bits=Serial.DATA_BITS_7,
        stop_bits=Serial.STOP_BITS_1,
        parity=Serial.PARITY_EVEN,
    )

    # constants useful for the serial communication protocol with an IKA device
    CR_HEX = "\x0d"  # carriage return
    LF_HEX = "\x0a"  # line feed or new line
    LINE_ENDING = CR_HEX + LF_HEX  # each individual command and each response are terminated CR LF
    LINE_ENDING_ENCODED = LINE_ENDING.encode()

    def __init__(self,
                 port: str,
                 dummy: bool = False,
                 ):
        """
        Abstract base class for an IKA device.

        :param str, port: port to connect to the device
        :param Path, str, database_path: file path to the database to store data during operation
        :param bool, dummy: if dummy is True then dont try to a serial device; used for unit tests
        """
        # storage variables
        self._port = port
        self._dummy = dummy

        try:
            # only connect to the serial device if the device is not a dummy device
            Serial.__init__(self,
                            port,
                            connect=not dummy,
                            **self.CONNECTION_SETTINGS)
        except Exception as e:
            logger.error(e)
            raise IKAError(msg=f'Unable to connect to an IKA device on port {port}. Make sure the device is '
                               'plugged in and the port is correct. If you meant to create a dummy instance, '
                               'instantiate a Dummy specific class or use the class method to get an instance')

        # lock for use when making serial requests
        self._lock = threading.Lock()

    @property
    def port(self):
        """Port used to connect to the IKA device"""
        return self._port

    @property
    def dummy(self) -> bool:
        """If dummy is True then dont try to a serial device"""
        return self._dummy

    def _format_request(self, data: str) -> bytes:
        """
        Format and encode a string to be sent to the device; commands are terminated with CR LF
        """
        data += self.LINE_ENDING
        return data.encode()

    def write(self, data: Union[bytes, str], timeout: Optional[NumberType]=None) -> int:
        """
        Write to a Serial device if it is not a dummy device. If data is a string it gets formatted and encoded to
        be sent to the device.

        :param data:
        :param timeout:
        :return:
        """
        if self.dummy is True:
            return 0
        else:
            if type(data) == str:
                data = self._format_request(data)
            return super().write(data, timeout)

    @abstractmethod
    def request(self,
                data: Union[bytes, str],
                timeout: Optional[NumberType] = None,
                line_ending: bytes = b'\r',
                ) -> Union[str, NumberType]:
        """
        The subclass should return this abstract method if the subclass is a dummy class, else the subclass should
        override this method, and include a call to this super in its implementation to handle making a request

        :param data: request data to write, in byte or string. if a string is provided, it will be formated by
            _format_request
        :param timeout: [Optional] read timeout to use when reading response
        :param line_ending: [Optional] line ending byte(s) to look for in response, defaults to ``b'\\r'``
        :return response from the device formatted; if a number is received as a response then return the value as
            the appropriate number type
        """
        if self.dummy is True:
            """Just return 0. The concrete classes should have their own implementations to simulate getting 
            properties of the device"""
            return 0
        else:
            return super().request(data, timeout, line_ending)
