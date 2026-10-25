"""Chart input / cached / thinking tokens per model call from session_calls.csv.

Usage (from gemini-cli-dissection/work/):
    python plot_context.py submission/session_calls.csv --out submission/context_growth.png

Also prints a Markdown table you can paste into writeup.md.
Needs matplotlib:  python -m pip install matplotlib
"""
import argparse
import csv


def to_int(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--out", default="context_growth.png")
    args = ap.parse_args()

    with open(args.csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("CSV is empty")

    calls = list(range(1, len(rows) + 1))
    inp = [to_int(r.get("input_token_count")) for r in rows]
    cached = [to_int(r.get("cached_content_token_count")) for r in rows]
    thoughts = [to_int(r.get("thoughts_token_count")) for r in rows]

    print("| call | model | input | cached | cached % | thoughts | output |")
    print("|---:|---|---:|---:|---:|---:|---:|")
    for i, r in enumerate(rows):
        pct = f"{100 * cached[i] / inp[i]:.0f}%" if inp[i] else "-"
        print(f"| {i + 1} | {r.get('model', '')} | {inp[i]} | {cached[i]} | {pct} | "
              f"{thoughts[i]} | {to_int(r.get('output_token_count'))} |")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(calls, inp, marker="o", label="input_token_count")
    ax.plot(calls, cached, marker="s", label="cached_content_token_count")
    ax.bar(calls, thoughts, alpha=0.3, label="thoughts_token_count")
    ax.set_xlabel("model call #")
    ax.set_ylabel("tokens")
    ax.set_title("Context growth across the Gemini CLI session")
    ax.set_xticks(calls)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(args.out, dpi=150)
    print(f"\nsaved chart to {args.out}")


if __name__ == "__main__":
    main()
