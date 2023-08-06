import time
import logging

from ika.thermoshaker import Thermoshaker

logger = logging.getLogger(__name__)
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=format, level=logging.DEBUG)


if __name__ == '__main__':
    port = 'COM8'  # todo set to the correct port
    dummy = True  # todo set to true if testing without connecting to an actual thermoshaker

    kwargs = {
        'port': port,
        'dummy': dummy,
    }
    ts = Thermoshaker.create(**kwargs)

    ts.watchdog_safety_temperature = 15.5
    ts.start_watchdog_mode_1(30)
    ts.start_watchdog_mode_2(30)
    ts.switch_to_normal_operation_mode()

    actual_temperature = ts.temperature
    set_temperature = ts.set_temperature
    actual_speed = ts.speed
    set_speed = ts.set_speed
    logger.info(f'actual temperature: {actual_temperature}, '
                f'set temperature: {set_temperature}, '
                f'actual speed: {actual_speed}, '
                f'set speed: {set_speed}')

    logger.info('change the set temperature to 30 and speed to 500')
    ts.set_temperature = 30
    ts.set_speed = 500
    set_temperature = ts.set_temperature
    set_speed = ts.set_speed
    logger.info(f'set temperature: {set_temperature}, '
                f'set speed: {set_speed}')

    logger.info('start tempering and shaking')
    ts.start_tempering()
    ts.start_shaking()

    time.sleep(5)

    actual_temperature = ts.temperature
    actual_speed = ts.speed
    logger.info(f'actual temperature: {actual_temperature}, '
                f'actual speed: {actual_speed}')

    logger.info('change the set temperature to 25 and speed 0')
    ts.set_temperature = 25
    ts.set_speed = 0
    set_temperature = ts.set_temperature
    set_speed = ts.set_speed
    logger.info(f'set temperature: {set_temperature}, '
                f'set speed: {set_speed}')
    actual_temperature = ts.temperature
    actual_speed = ts.speed
    logger.info(f'actual temperature: {actual_temperature}, '
                f'actual speed: {actual_speed}')

    logger.info('stop tempering and shaking')
    ts.stop_tempering()
    ts.stop_shaking()

