"""First-order radio energy model.

    E_tx(k, d) = E_elec*k + E_fs*k*d^2      if d <  d0
               = E_elec*k + E_mp*k*d^4      if d >= d0
    E_rx(k)    = E_elec*k
    E_da(k, s) = E_DA*k*s                   (aggregating s signals of k bits)
    d0         = sqrt(E_fs / E_mp)
"""
from __future__ import annotations

import numpy as np

from config import EnergyConfig


class EnergyModel:
    def __init__(self, cfg: EnergyConfig | None = None):
        cfg = cfg or EnergyConfig()
        self.e_elec = cfg.e_elec
        self.e_fs = cfg.e_fs
        self.e_mp = cfg.e_mp
        self.e_da = cfg.e_da
        self.d0 = float(np.sqrt(self.e_fs / self.e_mp))

    def tx_energy(self, bits, distance):
        """Energy to transmit ``bits`` over ``distance`` metres (scalar or array)."""
        d = np.asarray(distance, dtype=float)
        amp = np.where(d < self.d0, self.e_fs * d ** 2, self.e_mp * d ** 4)
        out = bits * (self.e_elec + amp)
        return float(out) if out.ndim == 0 else out

    def rx_energy(self, bits):
        return bits * self.e_elec

    def aggregation_energy(self, bits, signals=1):
        out = self.e_da * bits * np.asarray(signals, dtype=float)
        return float(out) if out.ndim == 0 else out
