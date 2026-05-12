# # audio.py
# import pygame
# import numpy as np

# class AudioManager:
#     def __init__(self):
#         self.enabled = True
#         self.current_track = None
#         self.music_playing = False
    
#     def _gen_tone(self, freq, dur, vol=0.3, wave='sine'):
#         if not self.enabled: 
#             return None
#         try:
#             t = np.linspace(0, dur, int(22050 * dur), False)
#             if wave == 'sine':
#                 w = np.sin(2 * np.pi * freq * t)
#             elif wave == 'square':
#                 w = np.sign(np.sin(2 * np.pi * freq * t))
#             else:
#                 w = np.sin(2 * np.pi * freq * t)
            
#             fade = np.linspace(1, 0, len(w))
#             audio = (w * fade * vol * 32767 * 0.5).astype(np.int16)
#             return pygame.sndarray.make_sound(np.column_stack((audio, audio)))
#         except Exception as e:
#             print(f"Audio error: {e}")
#             return None
    
#     def play_sfx(self, freq, dur, vol=0.3):
#         s = self._gen_tone(freq, dur, vol)
#         if s: 
#             s.set_volume(vol)
#             s.play()
    
#     def start_lobby_music(self):
#         if self.music_playing: 
#             return
#         try:
#             pygame.mixer.stop()
#             self.current_track = self._gen_ambient()
#             if self.current_track:
#                 self.current_track.set_volume(0.35)
#                 self.current_track.play(loops=-1)
#                 self.music_playing = True
#                 print("🎵 Lobby music started")
#         except Exception as e:
#             print(f"Music start failed: {e}")
    
#     def _gen_ambient(self):
#         sr, dur = 22050, 12.0
#         t = np.linspace(0, dur, int(sr * dur), False)
#         buf = np.zeros(len(t))
        
#         # Ambient chord progression
#         chords = [(110, 130.81, 164.81), (87.31, 110, 130.81), (130.81, 164.81, 196.00), (98.00, 123.47, 146.83)]
        
#         for i, (f1, f2, f3) in enumerate(chords):
#             s, e = i * int(sr * 3), (i + 1) * int(sr * 3)
#             chunk = t[s:e] - t[s]
#             env = np.ones(len(chunk))
#             env[:int(sr * 0.5)] = np.linspace(0, 1, int(sr * 0.5))
#             env[-int(sr * 0.5):] = np.linspace(1, 0, int(sr * 0.5))
            
#             buf[s:e] += 0.15 * np.sin(2 * np.pi * f1 * chunk) * env
#             buf[s:e] += 0.10 * np.sin(2 * np.pi * f2 * chunk) * env
#             buf[s:e] += 0.08 * np.sin(2 * np.pi * f3 * chunk) * env
        
#         buf = np.convolve(buf, np.ones(100) / 100, mode='same')
#         buf = buf / np.max(np.abs(buf)) * 0.5
#         audio16 = buf.astype(np.int16)
#         return pygame.sndarray.make_sound(np.column_stack((audio16, audio16)))
    
#     def stop_music(self, fade_ms=800):
#         if self.current_track and self.music_playing:
#             self.current_track.fadeout(fade_ms)
#             self.music_playing = False

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
        # Shorter duration for pure python generation to avoid hang
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
                # Envelope
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