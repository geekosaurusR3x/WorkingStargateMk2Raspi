import config
from gpiozero import PWMLED
from time import sleep


class LightingControl:
    chevrons = [PWMLED(pin, frequency=10000) for pin in config.pins_chevron]
    gantry = PWMLED(config.pin_gantry, frequency=10000)
    wormhole = PWMLED(config.pin_wormhole, frequency=10000)

    # Constructor
    def __init__(self):
        # Ensure LEDs are all initially off
        for chevron in self.chevrons:
            chevron.off()
        self.gantry.off()

    # Cycle through each chevron in turn with a delay between each
    def cycle_chevrons(self):
        for led_num, chevron in enumerate(self.chevrons):
            print('LED: {}'.format(led_num + 1))
            chevron.on()
            sleep(5)
            chevron.off()

    # Turn on ALL lighting
    def all_on(self):
        self.gantry.on()
        self.all_chevrons_on()
        self.wormhole.on()

    # Turn off ALL lighting
    def all_off(self):
        self.wormhole.off()
        self.gantry.off()
        self.all_chevrons_off()
    
    # Turn on all chevrons
    def all_chevrons_on(self):
        for chevron in self.chevrons:
            chevron.on()
    
    # Turn off all chevrons
    def all_chevrons_off(self):
        for chevron in self.chevrons:
            chevron.off()
    
    # Enable a single chevron
    def light_chevron(self, index, exclusive=False, value=1):
        if exclusive:
            self.all_off()
        self.chevrons[index].value = value

    # Darken a single chevron
    def darken_chevron(self, index):
        self.chevrons[index].off()

    def light_gantry(self, value=1):
        self.gantry.value = value

    def darken_gantry(self):
        self.gantry.off()

    def light_wormhole(self):
        self.wormhole.on()

    def darken_wormhole(self):
        self.wormhole.off()
