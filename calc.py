from pathlib import Path
import toml

def sum_wc(path: Path) -> int:
    wc = 0

    if (path / ".metadata").exists():
        with open(path / ".metadata", "r", encoding="utf-8") as f:
            metadata = toml.load(f)
            wc += metadata["wc"]

    for p in path.iterdir():
        if p.is_dir():
            wc += sum_wc(p)
    
    return wc


if __name__ == "__main__":
    print(sum_wc(Path(__file__).parent))
