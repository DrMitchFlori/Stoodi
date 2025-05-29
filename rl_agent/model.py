"""Neural network architecture for policy and value estimation."""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class ResidualBlock(nn.Module):
    """A simple residual block used in the AlphaZero network."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        residual = x
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += residual
        return F.relu(x)


class AlphaZeroNetwork(nn.Module):
    """Minimal AlphaZero-style convolutional network."""

    def __init__(self, board_channels: int = 18, filters: int = 128, blocks: int = 5):
        super().__init__()
        self.conv = nn.Conv2d(board_channels, filters, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm2d(filters)
        self.res_blocks = nn.ModuleList([ResidualBlock(filters) for _ in range(blocks)])

        # Policy head
        self.policy_conv = nn.Conv2d(filters, 32, kernel_size=1)
        self.policy_bn = nn.BatchNorm2d(32)
        self.policy_fc = nn.Linear(32 * 8 * 8, 4672)

        # Value head
        self.value_conv = nn.Conv2d(filters, 32, kernel_size=1)
        self.value_bn = nn.BatchNorm2d(32)
        self.value_fc1 = nn.Linear(32 * 8 * 8, 128)
        self.value_fc2 = nn.Linear(128, 1)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        x = F.relu(self.bn(self.conv(x)))
        for block in self.res_blocks:
            x = block(x)

        # Policy
        p = F.relu(self.policy_bn(self.policy_conv(x)))
        p = p.view(p.size(0), -1)
        p = self.policy_fc(p)

        # Value
        v = F.relu(self.value_bn(self.value_conv(x)))
        v = v.view(v.size(0), -1)
        v = F.relu(self.value_fc1(v))
        v = torch.tanh(self.value_fc2(v))
        return p, v.squeeze(-1)
