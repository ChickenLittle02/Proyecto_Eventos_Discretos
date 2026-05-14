import numpy as np
import math

class RandomVars:
    def __init__(self, seed=None):
        self.rng = np.random.RandomState(seed)

    def uniform(self, a=0, b=1):
        """Genera una variable aleatoria uniforme en [a, b)"""
        return self.rng.uniform(a, b)

    def exponential(self, rate):
        """Genera una variable aleatoria exponencial con tasa 'rate' (media = 1/rate)"""
        u = self.uniform()
        return -math.log(u) / rate

    def normal_box_muller(self, mu=0, sigma=1):
        """Genera una variable aleatoria normal usando Box-Muller"""
        u1 = self.uniform()
        u2 = self.uniform()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return mu + sigma * z0

    def discrete(self, probs):
        """Genera una variable discreta dada una lista de probabilidades"""
        u = self.uniform()
        cumulative = 0
        for i, p in enumerate(probs):
            cumulative += p
            if u < cumulative:
                return i
        return len(probs) - 1  # fallback