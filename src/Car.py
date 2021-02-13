import time
import math
import threading

import Motor
import Ultrasonic
import servo
import ADC

Rad2Deg = 180 / math.pi

def clamp(x, min_, max_):
    return max(min_, min(x, max_))

def frange(start, stop, step):
    x = start
    while x <= stop:
        yield x
        x += step

class InterruptedException(Exception):
    pass

class Car:
    MotorFwd = 2000
    MotorSpeed = 0.85 #m/s
    TurnFwd = 2000
    TurnBack = -TurnFwd
    TurnRate = math.pi / 1.3 #rad/sec
    ServoTurnRate = math.pi / 4 #rad/sec
    
    def __init__(self):
        self._interrupted = False
        self._lock = threading.RLock()
        self._cmdThread = None
        self.motor = Motor.Motor()
        self.sonic = Ultrasonic.Ultrasonic()
        self.adc = ADC.Adc()
        self.servo = servo.Servo()
        self.stop()
        self.pointSonic()

    def sleep(self, seconds):
        ns = round(seconds * 1e9)
        start = time.perf_counter_ns()
        while not self.isInterrupted():
            now = time.perf_counter_ns()
            elapsed = now - start
            if elapsed >= ns:
                break
            time.sleep(min(0.005, (ns - elapsed) * 1e-9))
        if self.isInterrupted():
            raise InterruptedException("Interrupted by caller!")

    def isInterrupted(self):
        self._lock.acquire()
        res = self._interrupted
        self._lock.release()
        return res
        
    def interrupt(self):
        self._lock.acquire()
        self._interrupted = True
        self._lock.release()

    def isFinished(self):
        self._lock.acquire()
        res = self._finished
        self._lock.release()
        return res

    def setFinished(self, val):
        self._lock.acquire()
        self._finished = val
        self._lock.release()

    def stop(self):
        self.motor.setMotorModel(0, 0, 0, 0)

    def turn(self, radians):
        self.stop()
        if radians > 0:
            radians *= 1.17
        left, right = (self.TurnBack, self.TurnFwd) if radians >= 0 else (self.TurnFwd, self.TurnBack)
        self.motor.setMotorModel(left, left, right, right)
        self.sleep(abs(radians) / self.TurnRate)
        self.stop()

    def move(self, dist):
        self.stop()
        speed = self.MotorFwd * (1 if dist >= 0 else -1)
        self.motor.setMotorModel(speed, speed, speed, speed)
        self.sleep(abs(dist) / self.MotorSpeed)
        self.stop()

    def pointSonic(self, hdir = 0.0, vdir = 0.0):
        hdir = clamp(hdir, -math.pi/2, math.pi/2)
        vdir = clamp(vdir, -math.pi/10, math.pi/2)
        self.servo.setServoPwm('0', -hdir * Rad2Deg + 90, 5)
        self.servo.setServoPwm('1', vdir * Rad2Deg + 90, 10)
        self.hdir = hdir
        self.vdir = vdir
        
    def getServoTurnTime(self, angle):
        return angle / self.ServoTurnRate
    
    def getCameraTurnTime(self, hdir, vdir):
        deltaAng = max(abs(hdir - self.hdir), abs(vdir - self.vdir))
        return self.getServoTurnTime(deltaAng)
        
    def measureDistance(self, hdir = 0.0, vdir = 0.0, times = 3):
        turnTime = max(0.2, self.getCameraTurnTime(hdir, vdir))
        self.pointSonic(hdir, vdir)
        self.sleep(turnTime)
        meters = self.sonic.get_distance(times) / 100.0
        return meters

    def getBatteryVoltage(self, times = 3):
        v = 0
        for _ in range(times):
            v += self.adc.recvADC(2) * 3
        v /= times
        return v
        
    def scanSector(self, angleStart, angleEnd, angleStep = math.pi/(180/5)):
        dist = []
        for dir in frange(angleStart, angleEnd, angleStep):
            dist.append((dir, self.measureDistance(dir)))
        return dist

    def cmdThreadFunc(self, cmd):
        try:
            cmd()
            self.setFinished(True)
        except InterruptedException:
            print("Command interrupted!")
        finally:
            self.stop()

    def execCommand(self, cmd):
        if self._cmdThread:
            self.interrupt()
            self._cmdThread.join()
            self._cmdThread = None
            self._interrupted = False
            self._finished = False
        if not cmd:
            return
        self._cmdThread = threading.Thread(target=(lambda: self.cmdThreadFunc(cmd)))
        self._cmdThread.start()
        
# Test
if __name__ == '__main__':
    print("Testing sensor and motor functions")
    try:
        car = Car()
        car.stop()
        
        voltage = car.getBatteryVoltage()
        print(f"Battery level: {voltage}v")
        
        def cmdTest():
            print("Cmd start")
            car.sleep(5)
            print("Cmd end!")
            
        car.execCommand(cmdTest)
        time.sleep(1)
        car.execCommand(None)
        
        """
        for d in car.scanSector(-math.pi/3, 0):
            print("Distance:", d)
        """
    
        """
        fwd = 0.5
        print(f"Forward {fwd}m")
        car.move(fwd)
        time.sleep(1)

        print(f"Back {fwd}m")
        car.move(-fwd)
        time.sleep(1)

        turn = math.pi/2
        print(f"Turn left {turn*180/math.pi} deg")
        car.turn(turn)
        time.sleep(1)
        
        print(f"Turn right {turn*180/math.pi} deg")
        car.turn(-turn)
        time.sleep(1)

        print("Distance ahead:", car.measureDistance(0, 0))
        print("Distance left:", car.measureDistance(math.pi/6, 0))
        print("Distance right:", car.measureDistance(-math.pi/6, 0))
        time.sleep(1)
        """        
        
    except KeyboardInterrupt:
        pass
    finally:
        car.pointSonic()
        car.stop()

