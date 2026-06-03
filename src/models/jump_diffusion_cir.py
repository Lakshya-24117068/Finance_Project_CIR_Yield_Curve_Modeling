import numpy as np
from src.models.cir import CIRModel

class JumpDiffusionCIRModel:
    def __init__(self, cir_model: CIRModel, lambd: float = 0.1, mu_j: float = 0.02):
        """
        Jump-Diffusion CIR: dr_t = kappa*(theta - r_t)*dt + sigma*sqrt(r_t)*dW_t + dJ_t
        where dJ_t is a compound Poisson process with rate lambda and mean jump size mu_j.
        """
        self.cir = cir_model
        self.lambd = lambd
        self.mu_j = mu_j

    def update_params(self, kappa: float, theta: float, sigma: float, lambd: float, mu_j: float) -> None:
        self.cir.update_params(kappa, theta, sigma)
        self.lambd = lambd
        self.mu_j = mu_j
