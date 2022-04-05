from StargateControl import StargateControl
from time import sleep
import config


class DialProgram:
    is_dialing = False
    is_dialed = False

    def __init__(self, gateControl, lightControl, audio):
        self.gateControl = gateControl
        self.lightControl = lightControl
        self.audio = audio
        self.outConnected = False;

    def dial(self, address,dialFromBook = False):
        if(config.enable_network):
            self.outConnected = dialFromBook
        
        length = len(address);
        if (length < 7) or (length > 9):
            raise ValueError('Address length must be 7, 8, or 9')

        DialProgram.is_dialing = True
        self.lightControl.all_off()
        self.gateControl.move_home()

        direction = StargateControl.FORWARD

        for i, symbol in enumerate(address):
            self.audio.play_roll()
            sleep(config.audio_delay_time)
            self.gateControl.move_to_symbol(symbol, direction)
            self.audio.stop_roll()

            self.audio.play_chevron_lock()
            sleep(config.audio_delay_time)
            self.gateControl.lock_chevron()
            
            if(config.enable_network):
                if(i == 7 and not self.outConnected):
                    sleep(config.chevron_engage_time+6)
                    self.gateControl.unlock_chevron()
                    self.audio.play_chevron_unlock()
                    sleep(config.audio_delay_time)
                    break

            if config.enable_gary_jones and length == 7: # Not currently available for 8 or 9-symbol addresses
                # Wait for play_chevron_lock() to finish
                while self.audio.is_playing():
                    sleep(0.1)
                    continue
                self.audio.play_chevron(i+1)
                sleep(config.audio_delay_time)
                if i == 6: # Wait for "chevron 7 locked" before engaging wormhole
                    while self.audio.is_playing():
                        sleep(0.1)
                        continue
            else:
                sleep(config.chevron_engage_time)
            self.audio.play_chevron_unlock()
            sleep(config.audio_delay_time)
            if i == length-1:
                self.gateControl.unlock_chevron(False)
            else:
                self.gateControl.unlock_chevron()
            while self.audio.is_playing():
                sleep(0.01)
                continue
            #if i == length-1:
            #    break

            self.lightControl.light_chevron(config.chevron_light_order[i])

            if direction == StargateControl.FORWARD:
                direction = StargateControl.BACKWARD
            else:
                direction = StargateControl.FORWARD

        #if not connected return
        if(config.enable_network):
            if(not self.outConnected):
                self.lightControl.all_off()
                DialProgram.is_dialing = False
                return

        self.audio.play_open()
        self.lightControl.all_on()
        sleep(1)
        while self.audio.is_playing():
            sleep(0.1)
            continue

        
        if config.play_theme:
            self.audio.play_theme()

        while self.audio.is_playing():
            sleep(0.1)
            continue

        DialProgram.is_dialing = False

    def dialed(self,callback):
        DialProgram.is_dialed = True
        self.lightControl.all_off()

        for i in [4,5,6,7,1,2,3]:
            self.lightControl.light_chevron(i)
            self.audio.play_chevron_lock()
            while self.audio.is_playing():
                sleep(0.1)
                continue

        if(config.enable_network and callback is not None):
            callback()
        
        self.audio.play_open()
        self.lightControl.all_on()
        sleep(1)
        while self.audio.is_playing():
            sleep(0.1)
            continue
        
        DialProgram.is_dialed = False

    def close(self):
        self.audio.play_close()
        sleep(1)
        self.lightControl.all_off()