"""Configuration dataclass for the AlphaZero training pipeline."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Hyperparameters and path configuration."""

    # Training parameters
    learning_rate: float = 1e-3
    batch_size: int = 256
    weight_decay: float = 1e-4

    # MCTS parameters
    simulations: int = 800
    c_puct: float = 1.5

    # Data paths
    data_dir: Path = Path("data")
    model_dir: Path = Path("checkpoints")

    def ensure_dirs(self) -> None:
        """Create necessary directories if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.model_dir.mkdir(parents=True, exist_ok=True)
