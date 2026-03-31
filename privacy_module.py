import numpy as np

class PrivacyEngine:
    """Differential Privacy using NumPy and Laplace/Gaussian mechanism."""
    
    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5):
        self.epsilon = epsilon
        self.delta = delta

    def _calculate_scale(self, sensitivity: float, mechanism: str = 'laplace') -> float:
        if mechanism == 'laplace':
            return sensitivity / self.epsilon
        elif mechanism == 'gaussian':
            # Simplified canonical Gaussian scale for (epsilon, delta)-DP
            c = np.sqrt(2 * np.log(1.25 / self.delta))
            return c * sensitivity / self.epsilon
        raise ValueError("Mechanism must be 'laplace' or 'gaussian'")

    def add_laplace_noise(self, value: float, sensitivity: float = 1.0) -> float:
        """Add Laplace noise to a single numerical query for epsilon-DP."""
        scale = self._calculate_scale(sensitivity, 'laplace')
        noise = np.random.laplace(loc=0.0, scale=scale)
        return value + noise

    def add_gaussian_noise(self, value: float, sensitivity: float = 1.0) -> float:
        """Add Gaussian noise to a single numerical query for (epsilon, delta)-DP."""
        scale = self._calculate_scale(sensitivity, 'gaussian')
        noise = np.random.normal(loc=0.0, scale=scale)
        return value + noise

    def anonymize_average(self, values: list[float], clip_min: float, clip_max: float) -> float:
        """
        Calculates a differentially private average.
        Values are clipped to [clip_min, clip_max].
        Sensitivity of sum is (clip_max - clip_min).
        """
        if not values:
            return 0.0
            
        n = len(values)
        clipped_values = np.clip(values, clip_min, clip_max)
        
        # Calculate DP Sum
        sensitivity_sum = clip_max - clip_min
        dp_sum = self.add_laplace_noise(np.sum(clipped_values), sensitivity_sum)
        
        # In a strict setting, count 'n' is also perturbed, but we assume public 'n' here for simplicity.
        dp_average = dp_sum / n
        return max(clip_min, min(dp_average, clip_max)) # Ensure within bounds functionally
        
    def anonymize_count(self, count: int, sensitivity: float = 1.0) -> int:
        """
        Calculates a DP count. Sensitivity of a count query is usually 1.
        """
        dp_count = int(round(self.add_laplace_noise(count, sensitivity)))
        return max(0, dp_count) # Counts cannot be negative
