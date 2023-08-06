# -*- coding: utf-8 -*-

import torch
from torch import nn, Tensor

from torchnorms.tnorms.base import BaseTNorm

from typing import Optional


class SchweizerSklarTNorm(BaseTNorm):
    def __init__(self,
                 p: Optional[Tensor] = None,
                 default_p: float = 0.1) -> None:
        super().__init__()
        self.p = p
        if self.p is None:
            self.p = nn.Parameter(torch.tensor(default_p))
        assert len(self.p.shape) == 0

        self.relu = torch.nn.ReLU()
        self.eps = 0.001

    def __call__(self,
                 a: Tensor,
                 b: Tensor) -> Tensor:
        res: Optional[Tensor] = None
        # Careful that the value of parametr p can be 10e-8, thus maybe add eps.

        self.p.data = self.relu(self.p.data+3)-3
        if self.p == 0:
            self.p.data += self.eps

        # self.p.data = torch.clamp(self.p.data, min=-4)
        if torch.isnan(self.p):
            print("NAN a BRAT")
            self.p.data = torch.tensor(0.1)


        if self.p.item() < 0.0:
            res: Tensor = ((a ** self.p + b ** self.p) - 1.0) ** (1.0 / self.p)
        else:
            res: Tensor = (a ** self.p + b ** self.p) - 1.0
            res: Tensor = torch.maximum(res, torch.tensor(0.0))
            res: Tensor = res ** (1.0 / self.p)


        if torch.sum(torch.isnan(res)):
            print(a,b)
            print(self.p)
            print(res)
            print("GANDON NAN")

        return res
