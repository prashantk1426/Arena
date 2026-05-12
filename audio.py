# audio.py
import pygame
import math
import array

class AudioManager:
    def __init__(self):
        self.enabled = True
        self.current_track = None
        self.music_playing = False
        self.sample_rate = 22050

    def _gen_tone(self, freq, dur, vol=0.3, wave='sine'):
        num_samples = int(self.sample_rate * dur)
        samples = array.array('h', [0] * (num_samples * 2)) # Stereo
        
        for i in range(num_samples):
            t = i / self.sample_rate
            val = math.sin(2 * math.pi * freq * t)
            if wave == 'square':
                val = 1.0 if val >= 0 else -1.0
            
            # Linear Fade out
            fade = (num_samples - i) / num_samples
            
            # 16-bit signed integer conversion
            sample = int(val * fade * vol * 32767 * 0.5)
            samples[i*2] = sample     # Left
            samples[i*2 + 1] = sample # Right
            
        return pygame.mixer.Sound(buffer=samples)

    def play_sfx(self, freq, dur, vol=0.3):
        try:
            s = self._gen_tone(freq, dur, vol)
            s.play()
        except: pass

    def start_lobby_music(self):
        if self.music_playing: return
        try:
            pygame.mixer.stop()
            self.current_track = self._gen_ambient()
            if self.current_track:
                self.current_track.set_volume(0.3)
                self.current_track.play(loops=-1)
                self.music_playing = True
        except: pass

    def _gen_ambient(self):
        dur = 8.0
        num_samples = int(self.sample_rate * dur)
        samples = array.array('h', [0] * (num_samples * 2))
        
        chords = [(82.41, 110, 146.83), (73.42, 98, 130.81)]
        chord_dur = dur / len(chords)
        
        for c_idx, (f1, f2, f3) in enumerate(chords):
            start_s = int(c_idx * chord_dur * self.sample_rate)
            end_s = int((c_idx + 1) * chord_dur * self.sample_rate)
            
            for i in range(start_s, end_s):
                t = i / self.sample_rate
                rel_i = i - start_s
                chunk_len = end_s - start_s
                env = 1.0
                attack = int(self.sample_rate * 0.5)
                if rel_i < attack: env = rel_i / attack
                elif rel_i > chunk_len - attack: env = (chunk_len - rel_i) / attack
                
                val = (0.12 * math.sin(2 * math.pi * f1 * t) + 
                       0.08 * math.sin(2 * math.pi * f2 * t) + 
                       0.06 * math.sin(2 * math.pi * f3 * t)) * env
                
                sample = int(val * 32767 * 0.4)
                samples[i*2] = sample
                samples[i*2 + 1] = sample
                
        return pygame.mixer.Sound(buffer=samples)

    def stop_music(self, fade_ms=1000):
        if self.current_track and self.music_playing:
            self.current_track.fadeout(fade_ms)
            self.music_playing = False