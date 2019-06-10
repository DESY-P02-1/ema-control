"""
Robot class should create a socket and provide methods to use that socket to pass instructions through that socket to the robot.
Methods on the module should then use an instance of this class to send commands to achieve tasks

methods required:
X power_on
X power_off
X start
X stop
- set_axis
- homing
- power_status
- mount_sample
- unmount_sample
- (status)
- (calibrate_sam)
- (compare_sam)
"""


class Robot():

    def send(self, message):
        pass

    @staticmethod
    def samplenr_to_xy(n):
        """
        Convert the numerical index of the requested sample to xy coordinates
        on the sample magazine.

        Parameters
        ----------
        n : integer

        Returns
        -------
        tuple of integers : x & y coordinates

        Raises
        ------
        ValueError : if n is not greater than 0
        """
        # In the original code this was expressed as:
        # x=((n-1)/10)+1
        # y=((n-1)%10)+1
        if n <= 0:
            raise ValueError('Expecting value greater than 0')
        return (n // 10 + 1, n % 10)


def power_off():
    """
    Disables power to the robot.
    """
    ema.send('powerOff')


def power_on():
    """
    Enables power to the robot.
    """
    ema.send('powerOn')


def reset():
    # TODO: Needs doc
    ema.send('reset')


def restart():
    # TODO: Needs doc
    ema.send('restartMotor')


def start():
    # TODO: Needs doc
    ema.send('start')


def stop():
    # TODO: Needs doc
    ema.send('stopMotor')


ema = Robot()