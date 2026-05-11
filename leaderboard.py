# # leaderboard.py
# import pickle
# import os

# class Leaderboard:
#     def __init__(self, file='arena_scores.dat'):
#         self.file = file
#         self.scores = self._load()
#     def _load(self):
#         try:
#             if os.path.exists(self.file):
#                 with open(self.file, 'rb') as f: return pickle.load(f)
#         except: pass
#         return []
#     def save(self):
#         try:
#             with open(self.file, 'wb') as f: pickle.dump(self.scores[:20], f)
#         except: pass
#     def add(self, name, score, game):
#         self.scores.append({'name': name, 'score': score, 'game': game})
#         self.scores.sort(key=lambda x: x['score'], reverse=True)
#         self.scores = self.scores[:20]
#         self.save()

# leaderboard.py
import pickle
import os

class Leaderboard:
    def __init__(self, file='arena_scores.dat'):
        self.file = file
        self.scores = self._load()
    def _load(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, 'rb') as f: return pickle.load(f)
        except: pass
        return []
    def save(self):
        try:
            with open(self.file, 'wb') as f: pickle.dump(self.scores[:30], f)
        except: pass
    def add(self, name, score, game, difficulty):
        self.scores.append({'name': name, 'score': score, 'game': game, 'diff': difficulty})
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:30]
        self.save()