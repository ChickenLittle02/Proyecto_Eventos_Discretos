import sys
sys.path.append('/home/nebur02/Documents/3er Ano/2do SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src')

import unittest
import numpy as np
from random_vars import RandomVars
from scipy import stats


class TestRandomVars(unittest.TestCase):
    """Pruebas unitarias para los generadores de variables aleatorias"""

    def setUp(self):
        """Inicializa generador para cada test"""
        self.rng = RandomVars(seed=42)
        self.n_samples = 10000  # Número de muestras para tests estadísticos

    # ========== PRUEBAS DE UNIFORME ==========

    def test_uniform_range(self):
        """Verifica que uniform(a, b) está en [a, b)"""
        a, b = 0, 1
        samples = [self.rng.uniform(a, b) for _ in range(1000)]
        self.assertTrue(all(a <= s < b for s in samples))

    def test_uniform_mean(self):
        """Verifica que la media de uniform(0,1) es aproximadamente 0.5"""
        samples = [self.rng.uniform(0, 1) for _ in range(self.n_samples)]
        mean = np.mean(samples)
        # Media teórica de U(0,1) es 0.5
        self.assertAlmostEqual(mean, 0.5, delta=0.02)

    def test_uniform_variance(self):
        """Verifica que la varianza de uniform(0,1) es 1/12 ≈ 0.0833"""
        samples = [self.rng.uniform(0, 1) for _ in range(self.n_samples)]
        var = np.var(samples, ddof=1)
        theoretical_var = 1 / 12
        self.assertAlmostEqual(var, theoretical_var, delta=0.01)

    # ========== PRUEBAS DE EXPONENCIAL ==========

    def test_exponential_positive(self):
        """Verifica que exponential() siempre devuelve valores > 0"""
        rate = 1 / 20
        samples = [self.rng.exponential(rate) for _ in range(1000)]
        self.assertTrue(all(s > 0 for s in samples))

    def test_exponential_mean_20(self):
        """Verifica que exponential(1/20) tiene media ≈ 20"""
        rate = 1 / 20
        samples = [self.rng.exponential(rate) for _ in range(self.n_samples)]
        mean = np.mean(samples)
        # Media teórica es 1/rate = 20
        self.assertAlmostEqual(mean, 20, delta=1.0)

    def test_exponential_mean_15(self):
        """Verifica que exponential(1/15) tiene media ≈ 15"""
        rate = 1 / 15
        samples = [self.rng.exponential(rate) for _ in range(self.n_samples)]
        mean = np.mean(samples)
        self.assertAlmostEqual(mean, 15, delta=1.0)

    def test_exponential_ks_test(self):
        """Prueba Kolmogorov-Smirnov: verifica que samples siguen Exp(λ=1/20)"""
        rate = 1 / 20
        samples = [self.rng.exponential(rate) for _ in range(self.n_samples)]
        
        # Comparar con exponencial teórica (scipy)
        ks_stat, p_value = stats.kstest(samples, 'expon', args=(0, 20))
        
        # Si p > 0.05, no rechazamos H0 (sí es exponencial)
        self.assertGreater(p_value, 0.05, 
                          f"KS test failed: p-value = {p_value:.4f} (debe ser > 0.05)")

    # ========== PRUEBAS DE NORMAL ==========

    def test_normal_mean_5_sigma_2(self):
        """Verifica que normal(5, 2) tiene media ≈ 5"""
        samples = [self.rng.normal_box_muller(mu=5, sigma=2) 
                  for _ in range(self.n_samples)]
        mean = np.mean(samples)
        self.assertAlmostEqual(mean, 5, delta=0.1)

    def test_normal_std_5_sigma_2(self):
        """Verifica que normal(5, 2) tiene desviación ≈ 2"""
        samples = [self.rng.normal_box_muller(mu=5, sigma=2) 
                  for _ in range(self.n_samples)]
        std = np.std(samples, ddof=1)
        self.assertAlmostEqual(std, 2, delta=0.1)

    def test_normal_ks_test(self):
        """Prueba Kolmogorov-Smirnov: verifica que samples siguen N(5, 2)"""
        samples = [self.rng.normal_box_muller(mu=5, sigma=2) 
                  for _ in range(self.n_samples)]
        
        # Normalizar para comparar con N(0,1)
        normalized = (np.array(samples) - 5) / 2
        ks_stat, p_value = stats.kstest(normalized, 'norm')
        
        self.assertGreater(p_value, 0.05,
                          f"KS test failed: p-value = {p_value:.4f}")

    # ========== PRUEBAS DE DISCRETA ==========

    def test_discrete_returns_valid_index(self):
        """Verifica que discrete() devuelve índice válido"""
        probs = [0.45, 0.25, 0.10, 0.20]
        for _ in range(1000):
            result = self.rng.discrete(probs)
            self.assertIn(result, [0, 1, 2, 3])

    def test_discrete_probabilities(self):
        """Verifica que las probabilidades de discrete() son correctas"""
        probs = [0.45, 0.25, 0.10, 0.20]
        samples = [self.rng.discrete(probs) for _ in range(self.n_samples)]
        
        # Contar frecuencias
        counts = [samples.count(i) for i in range(4)]
        empirical_probs = np.array(counts) / self.n_samples
        
        # Comparar con probabilidades teóricas
        for i, (empirical, theoretical) in enumerate(zip(empirical_probs, probs)):
            self.assertAlmostEqual(empirical, theoretical, delta=0.02,
                                 msg=f"Índice {i}: empírica={empirical:.3f}, teórica={theoretical:.3f}")

    def test_discrete_cumsum_sums_to_one(self):
        """Verifica que las probabilidades sumen a 1"""
        probs = [0.45, 0.25, 0.10, 0.20]
        self.assertAlmostEqual(sum(probs), 1.0)

    # ========== PRUEBAS DE REPRODUCIBILIDAD ==========

    def test_reproducibility_with_seed(self):
        """Verifica que usar el mismo seed produce los mismos números"""
        rng1 = RandomVars(seed=123)
        rng2 = RandomVars(seed=123)
        
        samples1 = [rng1.exponential(0.1) for _ in range(100)]
        samples2 = [rng2.exponential(0.1) for _ in range(100)]
        
        np.testing.assert_array_equal(samples1, samples2)

    def test_different_seeds_different_results(self):
        """Verifica que diferentes seeds producen diferentes resultados"""
        rng1 = RandomVars(seed=123)
        rng2 = RandomVars(seed=456)
        
        samples1 = [rng1.exponential(0.1) for _ in range(100)]
        samples2 = [rng2.exponential(0.1) for _ in range(100)]
        
        # Deben ser diferentes (con probabilidad ~100%)
        self.assertFalse(np.allclose(samples1, samples2))


class TestRandomVarsEdgeCases(unittest.TestCase):
    """Pruebas de casos especiales y límites"""

    def setUp(self):
        self.rng = RandomVars(seed=42)

    def test_exponential_very_small_rate(self):
        """Exponencial con tasa muy pequeña (media muy grande)"""
        rate = 1 / 1000
        samples = [self.rng.exponential(rate) for _ in range(1000)]
        mean = np.mean(samples)
        self.assertGreater(mean, 500)  # Debe ser grande

    def test_normal_zero_mean_unit_variance(self):
        """Normal estándar N(0, 1)"""
        samples = [self.rng.normal_box_muller(mu=0, sigma=1) 
                  for _ in range(10000)]
        mean = np.mean(samples)
        std = np.std(samples, ddof=1)
        
        self.assertAlmostEqual(mean, 0, delta=0.05)
        self.assertAlmostEqual(std, 1, delta=0.05)

    def test_discrete_single_probability_1(self):
        """Discreto con una sola opción (probabilidad 1)"""
        result = self.rng.discrete([1.0])
        self.assertEqual(result, 0)

    def test_discrete_two_equal_probabilities(self):
        """Discreto con dos opciones igualmente probables"""
        probs = [0.5, 0.5]
        samples = [self.rng.discrete(probs) for _ in range(10000)]
        
        count_0 = samples.count(0)
        count_1 = samples.count(1)
        
        # Deben estar aproximadamente iguales
        self.assertAlmostEqual(count_0 / len(samples), 0.5, delta=0.05)


if __name__ == '__main__':
    # Ejecutar con nivel de detalle
    unittest.main(verbosity=2)
