# RL Agent Overview

This directory contains a minimal scaffold for an AlphaZero-style reinforcement learning setup using Stockfish as the chess environment.

## Directory Structure

- `config.py` – hyperparameters and path configuration.
- `model.py` – PyTorch neural network with policy and value heads.
- `mcts.py` – Monte Carlo Tree Search implementation.
- `self_play.py` – self-play loop using Stockfish.
- `train.py` – training routines for the neural network.
- `evaluate.py` – utilities for Elo evaluation.

These modules are intentionally lightweight and meant to be expanded upon. Stockfish binaries should be placed in a separate `stockfish/` directory.
