from AnimChase import AnimChase
from AnimRing import AnimRing
from AnimClock import AnimClock
from time import sleep
import config


# self.state values:
# 0: animation chase
# 1: animation ring
# 2: dial
# 3: animation clock
# 4: testing/debug
# 5: all lights off
# 6: do nothing

class StargateLogic:
    def __init__(self, audio, light_control, stargate_control, dial_program):
        self.audio = audio
        self.light_control = light_control
        self.stargate_control = stargate_control
        self.dial_program = dial_program
        self.anim_chase = AnimChase(light_control)
        self.anim_ring = AnimRing(light_control)
        self.anim_clock = AnimClock(light_control)
        self.state = 5
        self.address = []
        self.state_changed = True

    def execute_command(self, command):
        self.state_changed = True
        self.state = command['anim']

        if self.state == 2:
            address = command['sequence']
            #if len(address) != 7:
            if len(address) < 7:
                self.state = 0
                return
            self.address = address
        
        elif self.state == 4:
            self.state = 6
            action = command['action']
            
            if action == "spinBackward":
                #self.stargate_control.motor_gate.step(self.stargate_control.steps_per_symbol, config.gate_backward, config.motor_drive)
                self.stargate_control.motor_gate.step(20, config.gate_backward, config.motor_drive)
                self.stargate_control.release_motor(self.stargate_control.motor_gate)
            
            elif action == "spinForward":
                #self.stargate_control.motor_gate.step(self.stargate_control.steps_per_symbol, config.gate_forward, config.motor_drive)
                self.stargate_control.motor_gate.step(20, config.gate_forward, config.motor_drive)
                self.stargate_control.release_motor(self.stargate_control.motor_gate)
            
            elif action =="driveTest":
                self.stargate_control.drive_test()
            
            elif action == "goHome":
                self.stargate_control.move_home()
                
            elif action == "lockChevron":
                self.stargate_control.lock_chevron(0)
                sleep(1)
                self.stargate_control.unlock_chevron(0)
                
            elif action == "allLightsOn":
                self.light_control.all_on()
                
            elif action == "allLightsOff":
                self.light_control.all_off()
            
            elif action == "ringOn":
                self.light_control.light_chevron(0)
                self.light_control.light_chevron(1)
                self.light_control.light_chevron(2)
                self.light_control.light_chevron(3)
                self.light_control.light_chevron(4)
                self.light_control.light_chevron(5)
                self.light_control.light_chevron(6)
                self.light_control.light_chevron(7)
                self.light_control.light_chevron(8)
            
            elif action == "ringOff":
                self.light_control.darken_chevron(0)
                self.light_control.darken_chevron(1)
                self.light_control.darken_chevron(2)
                self.light_control.darken_chevron(3)
                self.light_control.darken_chevron(4)
                self.light_control.darken_chevron(5)
                self.light_control.darken_chevron(6)
                self.light_control.darken_chevron(7)
                self.light_control.darken_chevron(8)
            
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

            # Call relevant logic depending on state
            if self.state == 2:
                self.light_control.all_off()
                self.dial_program.dial(self.address)
                self.state = 5
            elif self.state == 0:
                delay = self.anim_chase.animate(state_changed)
                sleep(delay)
            elif self.state == 1:
                delay = self.anim_ring.animate(state_changed)
                sleep(delay)
            elif self.state == 3:
                delay = self.anim_clock.animate(state_changed)
                sleep(delay)
            elif self.state == 5:
                self.light_control.all_off()
                sleep(1)
            else:
                sleep(1)
