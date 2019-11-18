from datetime import datetime
import json

from shared.observable import Observable

class ServiceStatus(Observable):
    """Keep the global state of the service, so we can serve it up when a client
    needs to know when a device is online.
    """

    def __init__(self, sensor_limits):
        super(ServiceStatus, self).__init__(self)
        self.sensor_limits = sensor_limits
        self.is_database_connected = False
        self.relative_humidity = ''
        self.temperature = ''
        self.recorded_on = datetime.now()
        self.is_temperature_above_limit = False
        self.is_temperature_below_limit = False
        self.is_relative_humidity_above_limit = False
        self.is_relative_humidity_below_limit = False

    def should_show_warning_led(self):
        if (self.is_relative_humidity_above_limit or 
            self.is_relative_humidity_below_limit or 
            self.is_temperature_above_limit or 
            self.is_temperature_below_limit):
            return True

        return False

    def update_from_log_entry(self, entry):
        self.relative_humidity = entry.relative_humidity
        self.temperature = entry.temperature
        self.recorded_on = entry.recorded_on
        self.notify()

    def check_environment_limits(self, log_entry):
        if not self.sensor_limits:
            return

        humidity_limits = self.sensor_limits['RelativeHumidity']
        if humidity_limits:
            if humidity_limits['Max'] and log_entry.relative_humidity > humidity_limits['Max']:
                self.is_relative_humidity_above_limit = True
            else:
                self.is_relative_humidity_above_limit = False

            if humidity_limits['Min'] and log_entry.relative_humidity < humidity_limits['Min']:
                self.is_relative_humidity_below_limit = True
            else:
                self.is_relative_humidity_below_limit = False

        temp_limits = self.sensor_limits['Temperature']
        if temp_limits:
            if temp_limits['Max'] and log_entry.temperature > temp_limits['Max']:
                self.is_temperature_above_limit = True
            else:
                self.is_temperature_above_limit = False

            if temp_limits['Min'] and log_entry.temperature < temp_limits['Min']:
                self.is_temperature_below_limit = True
            else:
                self.is_temperature_below_limit = False

        self.notify()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        warnings = []

        if self.is_relative_humidity_above_limit: warnings.append('relative_humidity_above_limit')
        if self.is_relative_humidity_below_limit: warnings.append('relative_humidity_below_limit')
        if self.is_temperature_above_limit: warnings.append('temperature_above_limit')
        if self.is_temperature_below_limit: warnings.append('temperature_below_limit')

        return json.dumps({
            "isDatabaseConnected": self.is_database_connected,
            "relativeHumidity": self.relative_humidity.__str__(),
            "temperature": self.temperature.__str__(),
            "recordDateTime": self.recorded_on.ctime() if self.recorded_on else '',
            "warnings": warnings
        })