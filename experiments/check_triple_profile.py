"""Seeded regression evidence for note 001; floating point is not proof."""
import argparse
import json
from pathlib import Path
import platform

import numpy as np


def psi(x):
    x = np.asarray(x)
    return np.where(x <= 2, (x - 1) ** 2, 2 * x - 3)


def profile(e):
    return 2 * e - max(0.0, np.sqrt(4 * e / 3) - 1) ** 2


def metrics(g):
    eig = np.linalg.eigvalsh(g)
    e = float(np.sum(np.abs(np.triu(g, 1)) ** 2))
    return e, float(np.sum(psi(eig)))


def random_gram(rng, n=3):
    rank = int(rng.integers(1, n + 1))
    x = rng.normal(size=(rank, n)) + 1j * rng.normal(size=(rank, n))
    x /= np.linalg.norm(x, axis=0)
    return x.conj().T @ x


def run(samples, seed):
    rng = np.random.default_rng(seed)
    worst = float("inf")
    worst_pinching = float("inf")
    equality_error = 0.0
    for _ in range(samples):
        g = random_gram(rng)
        e, delta = metrics(g)
        worst = min(worst, delta - profile(e))
        if delta + 1e-10 < profile(e):
            raise AssertionError((g, e, delta))
    for r in np.linspace(0, 1, 1001):
        g = (1-r) * np.eye(3) + r * np.ones((3, 3))
        e, delta = metrics(g)
        equality_error = max(equality_error, abs(delta - profile(e)))
    for _ in range(max(1, samples // 10)):
        g = random_gram(rng, n=9)
        delta = float(np.sum(psi(np.linalg.eigvalsh(g))))
        bound = sum(profile(metrics(g[i:i+3, i:i+3])[0]) for i in (0, 3, 6))
        worst_pinching = min(worst_pinching, delta - bound)
        if delta + 1e-9 < bound:
            raise AssertionError("block profile inequality failed")
    if equality_error > 1e-10:
        raise AssertionError("equality family failed")
    return {
        "status": "passed", "evidence": "floating-point regression, not proof",
        "seed": seed, "complex_gram_samples": samples,
        "block_samples": max(1, samples // 10), "equality_samples": 1001,
        "minimum_profile_margin": worst,
        "minimum_block_margin": worst_pinching,
        "maximum_equality_error": equality_error,
        "python": platform.python_version(), "numpy": np.__version__,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20261004)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.samples < 1:
        parser.error("samples must be positive")
    result = run(args.samples, args.seed)
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
