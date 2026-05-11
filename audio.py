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
import numpy as np

class AudioManager:
    def __init__(self):
        self.enabled = True
        self.current_track = None
        self.music_playing = False
        try: self.np = np
        except ImportError: self.enabled = False

    def _gen_tone(self, freq, dur, vol=0.3, wave='sine'):
        if not self.enabled: return None
        t = self.np.linspace(0, dur, int(22050 * dur), False)
        w = self.np.sin(2 * self.np.pi * freq * t) if wave == 'sine' else self.np.sign(self.np.sin(2 * self.np.pi * freq * t))
        fade = self.np.linspace(1, 0, len(w))
        audio = (w * fade * vol * 32767 * 0.5).astype(self.np.int16)
        return pygame.sndarray.make_sound(self.np.column_stack((audio, audio)))

    def play_sfx(self, freq, dur, vol=0.3):
        s = self._gen_tone(freq, dur, vol)
        if s: s.set_volume(vol); s.play()

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
        sr, dur = 22050, 16.0
        t = self.np.linspace(0, dur, int(sr * dur), False)
        buf = self.np.zeros(len(t))
        chords = [(82.41,110,146.83), (73.42,98,130.81), (98,130.81,174.61), (87.31,116.54,155.56)]
        for i, (f1,f2,f3) in enumerate(chords):
            s, e = i*int(sr*4), (i+1)*int(sr*4)
            chunk = t[s:e] - t[s]
            env = self.np.ones(len(chunk))
            env[:int(sr*0.8)] = self.np.linspace(0,1,int(sr*0.8))
            env[-int(sr*0.8):] = self.np.linspace(1,0,int(sr*0.8))
            buf[s:e] += 0.12*self.np.sin(2*self.np.pi*f1*chunk)*env + 0.08*self.np.sin(2*self.np.pi*f2*chunk)*env + 0.06*self.np.sin(2*self.np.pi*f3*chunk)*env
        buf = self.np.convolve(buf, self.np.ones(200)/200, mode='same')
        buf = buf / self.np.max(self.np.abs(buf)) * 0.4
        return pygame.sndarray.make_sound(self.np.column_stack((buf.astype(self.np.int16), buf.astype(self.np.int16))))

    def stop_music(self, fade_ms=1000):
        if self.current_track and self.music_playing:
            self.current_track.fadeout(fade_ms)
            self.music_playing = False