"""Synthetic benchmark. Does not read or write the submitted state.json."""
from pathlib import Path
import contextlib
import gc
import hashlib
import importlib.util
import io
import json
import platform
import random
import statistics
import sys
import tempfile
import time
import tracemalloc


def measure(action):
    times, peaks = [], []
    for _ in range(5):
        gc.collect()
        tracemalloc.start()
        start = time.perf_counter()
        value = action()
        times.append((time.perf_counter() - start) * 1000)
        peaks.append(tracemalloc.get_traced_memory()[1])
        tracemalloc.stop()
    return value, {"median_ms": round(statistics.median(times), 3), "max_peak_kib": round(max(peaks) / 1024, 2)}


def main():
    project = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    source = project / "main.py"
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("quiz_benchmark_target", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix="benchmark-", dir=output.parent) as folder:
        state_path = Path(folder) / "state.json"
        with contextlib.redirect_stdout(io.StringIO()):
            game = module.QuizGame(state_path)
            game.quizzes = [module.Quiz(f"성능 측정용 문제 {i + 1}: 1 + 1은?", ["1", "2", "3", "4"], 2, "1 다음의 자연수") for i in range(1000)]
            game.history = [{"played_at": "2026-11-04T21:00:00+09:00", "total_questions": 10, "correct_count": 8, "score": 7} for _ in range(1000)]
            game.best_score, game.played_count = 7, 1000
            success, save_stats = measure(game.save_state)
            assert success
            reloaded, load_stats = measure(lambda: module.QuizGame(state_path))
            assert len(reloaded.quizzes) == len(reloaded.history) == 1000
            assert reloaded.best_score == 7 and reloaded.quizzes[-1].hint == "1 다음의 자연수"
            selected, sample_stats = measure(lambda: random.sample(reloaded.quizzes, 100))
            assert len({id(quiz) for quiz in selected}) == 100
            result = {
                "python": platform.python_version(), "platform": platform.system(),
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "synthetic_quizzes": 1000, "synthetic_history_records": 1000,
                "sample_count": 100, "repeats": 5,
                "file_bytes": state_path.stat().st_size,
                "save": save_stats, "load": load_stats, "sample": sample_stats,
                "notes": "Synthetic data; warm local filesystem; time includes tracemalloc overhead; peak is Python-tracked incremental allocations, not total process RAM. No console rendering or user input measured."
            }
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
