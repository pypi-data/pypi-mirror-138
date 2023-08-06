from robomaster import robot, config


class MarkerInfo:

    def __init__(self, x, y, w, h, info):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._info = info

    @property
    def pt1(self):
        return int((self._x - self._w / 2) * 1280), int((self._y - self._h / 2) * 720)

    @property
    def pt2(self):
        return int((self._x + self._w / 2) * 1280), int((self._y + self._h / 2) * 720)

    @property
    def center(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def text(self):
        return self._info

    @property
    def is_left(self):
        return self._x < 0.4

    @property
    def is_right(self):
        return self._x > 0.6


class SimpleRobot(object):

    @property
    def chassis(self):
        return self._robot.chassis

    @property
    def vision(self):
        return self._robot.vision

    @property
    def camera(self):
        return self._robot.camera

    @property
    def gimbal(self):
        return self._robot.gimbal

    @property
    def blaster(self):
        return self._robot.blaster

    @property
    def led(self):
        return self._robot.led

    @property
    def sensor(self):
        return self._robot.sensor

    def __init__(self, ip=None):
        if ip:
            config.ROBOT_DEFAULT_WIFI_ADDR = (ip, config.ROBOT_DEVICE_PORT)
        self._robot = robot.Robot()

    def __del__(self):
        self.stop()

    def start(self):
        self._robot.initialize(conn_type="ap")

    # ep_chassis.move(x=0, y=0, z=72, xy_speed=0.7,z_speed=50).wait_for_completed()
    def stop(self):
        # self.vision.unsub_detect_info(name="marker")
        # self.camera.stop_video_stream()
        self._robot.close()

    def forward(self, distance, speed=0.8):
        if distance > 0:
            try:
                self.chassis.move(distance / 100, 0, 0, speed).wait_for_completed()
            except:
                print('Forward -- Max value 500')
        else:
            print('Forward -- Entered value is negative')

    def backward(self, distance, speed=0.8):
        if distance > 0:
            self.chassis.move(0 - distance / 100, 0, 0, speed).wait_for_completed()
        else:
            raise (Exception("Negative Distance"))

    def left(self, distance, speed=0.8):
        if distance > 0:
            try:
                self.chassis.move(0, 0 - distance / 100, 0, speed).wait_for_completed()
            except:
                print('Left -- Max value 500')
        else:
            print('Left -- Entered value is negative')

    def right(self, distance, speed=0.8):
        if distance > 0:
            try:
                self.chassis.move(0, distance / 100, 0, speed).wait_for_completed()
            except:
                print('Right -- Max value 500')
        else:
            print('Right -- Entered value is negative')

    def clockwise(self, degree, speed=50):
        if degree > 0:
            try:
                self.chassis.move(0, 0, degree, 0, speed).wait_for_completed()
            except:
                print('Clockwise -- Max value 1800')
        else:
            print('Clockwise -- Entered value is negative')

    def anticlockwise(self, degree, speed=50):
        if degree > 0:
            try:
                self.chassis.move(0, 0, 0 - degree, 0, speed).wait_for_completed()
            except:
                print('Anticlockwise -- Max value 1800')
        else:
            print('Clockwise -- Entered value is negative')

    def gimbal_up(self, pitch):
        self.gimbal.move(pitch).wait_for_completed()

    def gimbal_down(self, pitch):
        self.gimbal.move(0 - pitch).wait_for_completed()

    def gimbal_right(self, yaw):
        self.gimbal.move(0, yaw).wait_for_completed()

    def gimbal_left(self, yaw):
        self.gimbal.move(0, 0 - yaw).wait_for_completed()

    def gimbal_recenter(self):
        self.gimbal.recenter().wait_for_completed()

    def fire(self, times, type='ir'):
        self.blaster.fire(fire_type=type, times=times)

    def led_red(self, effect='on', comp='all', red=0):
        red = 255
        self.led.set_led(comp=comp, r=red, g=0, b=0, effect=effect, freq=1)

    def led_blue(self, effect='on', comp='all'):
        self.led.set_led(comp=comp, r=0, g=0, b=255, effect=effect, freq=1)

    def led_green(self, effect='on', comp='all'):
        r = 0
        g = 0
        b = 0
        self.led.set_led(comp=comp, r=0, g=255, b=0, effect=effect, freq=1)

    def startVideo(self, diplay=False):
        self.camera.start_video_stream(display=diplay)

    def getFrame(self, timeout=0):
        return self.camera.read_cv2_image(strategy="newest", timeout=timeout)

    def detectMarkers(self):
        markers = []

        def on_detect_marker(marker_info):
            markers.clear()
            for i in range(0, len(marker_info)):
                x, y, w, h, info = marker_info[i]
                markers.append(MarkerInfo(x, y, w, h, info))
                # print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))

        result = self.vision.sub_detect_info(name="marker", callback=on_detect_marker)
        return markers
