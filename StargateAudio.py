import pygame, glob, random

# Note: pygame.mixer.Sound can only use wav or ogg, but can play multiple sounds at a time
# The wav files must be 16-bit.
# pygame.mixer.music can load mp3, but can only play one sound at a time

class StargateAudio:
    def __init__(self):
        pygame.mixer.init(44100, -16, 2, 4096)
        self.chevron_files = []
        # In chevron_files[0], store any extraneous sound clips (for use with manual lock/unlock)
        # Globs can't really exclude patterns, so grab ALL the files as a set, and then "subtract"
        # a set of the normal chevron clips. Lastly, save the set as a list, in chevron_files[0].
        chevron_files_0 = set(glob.glob('audio/walter/*.wav'))
        chevron_files_0 -= set(glob.glob('audio/walter/*c[1-9].wav'))
        self.chevron_files.append(list(chevron_files_0))
        # Now store the chevron-specific filenames
        for i in range(1,8):
            self.chevron_files.append(glob.glob('audio/walter/*c{}.wav'.format(i)))
        #print(self.chevron_files)
        self.unlock = pygame.mixer.Sound('audio/chev2.wav')
        self.lock = pygame.mixer.Sound('audio/chev1.wav')

    def is_playing(self):
        return pygame.mixer.get_busy() or pygame.mixer.music.get_busy()

    def play_roll(self):
        pygame.mixer.stop()
        pygame.mixer.music.load('audio/roll.mp3')
        pygame.mixer.music.play()

    def stop_roll(self):
        pygame.mixer.music.fadeout(200)
        while pygame.mixer.music.get_busy():
            continue

    def play_chevron_lock(self):
        self.lock.play()

    def play_chevron_unlock(self):
        self.unlock.play()

    def play_open(self):
        pygame.mixer.stop()
        pygame.mixer.music.load('audio/open.mp3')
        pygame.mixer.music.play()

    def play_close(self):
        pygame.mixer.stop()
        pygame.mixer.music.load('audio/close.mp3')
        pygame.mixer.music.play()

    def play_theme(self):
        pygame.mixer.stop()
        pygame.mixer.music.load('audio/sg1thm.mp3')
        pygame.mixer.music.play()

    def play_chevron(self, chevron):
        file = random.choice(self.chevron_files[chevron])
        #print("file: {}".format(file))
        chevron_sound = pygame.mixer.Sound(file)
        chevron_sound.play()