from enum import Enum
import time
from AnimChase import AnimChase
from AnimRing import AnimRing
from AnimClock import AnimClock
import config, random


# self.state values:
# 0: animation chase
# 1: animation ring
# 2: dial
# 3: animation clock
# 4: testing/debug
# 5: all lights off
# 6: do nothing
class StargateState(Enum):
    TESTDEBUG=-1
    IDLE=0
    DIAL=1
    OPEN=2
    CLOSE=3
    ANIMCHASE=10
    ANIMRING=11
    ANIMCLOCK=12
    ALLOFF=13

class StargateLogic:
    CONST_OPENTIME_INTERFACE = 2
    CONST_OPENTIME_NETWORK = 10

    def __init__(self, audio, light_control, stargate_control, dial_program,stargate_network):
        self.audio = audio
        self.light_control = light_control
        self.stargate_control = stargate_control
        self.dial_program = dial_program
        self.stargate_network = stargate_network
        self.anim_chase = AnimChase(light_control)
        self.anim_ring = AnimRing(light_control)
        self.anim_clock = AnimClock(light_control)
        self.state = StargateState.IDLE
        self.address = []
        self.state_changed = True
        self.callbackDial = None
        self.openTime = 0

        self.stargate_network.onIncomingConnection += self.dialFromNetwork
        self.stargate_network.onIncomingDisconnection += self.closeFromNetwork

    def dialFromNetwork(self, sequence,callback):
        self.address = list(map(int,sequence.split('.')))
        self.callbackDial = callback
        self.state = StargateState.DIAL
    
    def closeFromNetwork(self):
        self.state = StargateState.CLOSE

    def execute_command(self, command):
        self.state_changed = True
        self.state = StargateState(command['anim'])
        if self.state == StargateState.DIAL:
            address = command['sequence']
            #if len(address) != 7:
            if len(address) < 7:
                self.state = StargateState.ANIMCHASE
                return
            self.address = address
            self.callbackDial = None

        elif self.state == StargateState.TESTDEBUG:
            self.state = StargateState.IDLE
            action = command['action']
            
            if action == "spinBackward":
                self.stargate_control.motor_gate.step(round(self.stargate_control.steps_per_symbol), config.gate_backward, config.motor_drive)
                #self.stargate_control.motor_gate.step(20, config.gate_backward, config.motor_drive)
                self.stargate_control.release_motor(self.stargate_control.motor_gate)
            
            elif action == "spinForward":
                self.stargate_control.motor_gate.step(round(self.stargate_control.steps_per_symbol), config.gate_forward, config.motor_drive)
                #self.stargate_control.motor_gate.step(20, config.gate_forward, config.motor_drive)
                self.stargate_control.release_motor(self.stargate_control.motor_gate)
            
            elif action =="driveTest":
                self.stargate_control.drive_test()
            
            elif action == "goHome":
                self.stargate_control.move_home()
                
            elif action == "lockChevron":
                self.stargate_control.lock_chevron()
                if config.enable_gary_jones:
                    chevron = random.randrange(len(self.audio.chevron_files))
                    self.audio.play_chevron(chevron)
                    while self.audio.is_playing():
                        time.sleep(0.1)
                        continue
                else:
                    time.sleep(1)
                self.stargate_control.unlock_chevron()
                
            elif action == "allLightsOn":
                self.light_control.all_on()
                
            elif action == "allLightsOff":
                self.light_control.all_off()
            
            elif action == "ringOn":
                self.light_control.all_chevrons_on()
            
            elif action == "ringOff":
                self.light_control.all_chevrons_off()
            
            elif action == "rampOn":
                self.light_control.light_gantry()
            
            elif action == "rampOff":
                self.light_control.darken_gantry()
            
            elif action == "ledOn":
                self.stargate_control.cal_led.on()
            
            elif action == "ledOff":
                self.stargate_control.cal_led.off()
            
            elif action == "wormholeOn":
                self.light_control.light_wormhole()
            
            elif action == "wormholeOff":
                self.light_control.darken_wormhole()
                
            elif action == "chevron0":
                self.light_control.light_chevron(0)
            
            elif action == "chevron1":
                self.light_control.light_chevron(1)
            
            elif action == "chevron2":
                self.light_control.light_chevron(2)
            
            elif action == "chevron3":
                self.light_control.light_chevron(3)
            
            elif action == "chevron4":
                self.light_control.light_chevron(4)
            
            elif action == "chevron5":
                self.light_control.light_chevron(5)
            
            elif action == "chevron6":
                self.light_control.light_chevron(6)
            
            elif action == "chevron7":
                self.light_control.light_chevron(7)
            
            elif action == "chevron8":
                self.light_control.light_chevron(8)


    def loop(self):
        while True:
            state_changed = self.state_changed
            self.state_changed = False

            if(self.state == StargateState.OPEN):
                diff = self.CONST_OPENTIME_INTERFACE if(self.callbackDial is None) else self.CONST_OPENTIME_NETWORK
                if(self.openTime + diff < time.time()):
                    self.state = StargateState.CLOSE

            # Call relevant logic depending on state
            if self.state == StargateState.DIAL:
                self.light_control.all_off()
                self.dial_program.dial(self.address,self.callbackDial)
                self.state = StargateState.OPEN
                self.openTime = time.time()
            elif self.state == StargateState.ANIMCHASE:
                delay = self.anim_chase.animate(state_changed)
                time.sleep(delay)
            elif self.state == StargateState.ANIMRING:
                delay = self.anim_ring.animate(state_changed)
                time.sleep(delay)
            elif self.state == StargateState.ANIMCLOCK:
                delay = self.anim_clock.animate(state_changed)
                time.sleep(delay)
            elif self.state == StargateState.CLOSE:
                self.dial_program.close()
                self.state = StargateState.IDLE
            elif self.state == StargateState.ALLOFF:
                self.light_control.all_off()
            
            time.sleep(1)
