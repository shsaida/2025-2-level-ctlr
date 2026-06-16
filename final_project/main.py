"""
Final project implementation.
"""

# pylint: disable=unused-import
from pathlib import Path
from lab_6_pipeline.pipeline import UDPipeAnalyzer


def main(corpus_path: Path, dist_path: Path) -> None:
    """
    Generate conllu file for provided corpus of texts.

    Args:
        corpus_path (Path): Path to folder containing text files.
        dist_path (Path): Path to folder for saving auto_annotated.conllu.
    """
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus folder does not exist: {corpus_path}")
    
    txt_files = list(corpus_path.glob("*.txt"))
    if not txt_files:
        raise ValueError(f"No .txt files found in {corpus_path}")
    
    dist_path.mkdir(parents=True, exist_ok=True)

    output_file = corpus_path / "merged.txt"
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file in sorted(corpus_path.glob("*.txt")):
            content = file.read_text(encoding='utf-8')
            outfile.write(content)
            if not content.endswith('\n'):
                outfile.write('\n')
            print(f"Added: {file.name}")
    
    if not output_file.exists():
        raise FileNotFoundError(f"File {output_file} is not created")
    
    all_text = output_file.read_text(encoding='utf-8')
    if not all_text.strip():
        raise ValueError("Merged file is empty")
    
    analyzer = UDPipeAnalyzer()

    files_to_process = [f for f in txt_files if f.name != "merged.txt"]

    analyzer = UDPipeAnalyzer()

    all_conllu = []
    for i, file in enumerate(files_to_process, 1):
        print(f"Processing {i}/{len(files_to_process)}: {file.name}")
        try:
            text = file.read_text(encoding="utf-8").strip()
            if not text:
                print(f"Skipping empty file: {file.name}")
                continue
            annotated = analyzer.analyze([text])
            if annotated and annotated[0]:
                all_conllu.append(annotated[0])
        except Exception as e:
            print(f"Error in {file.name}: {e}")

    result = "\n".join(all_conllu)
    if not result.strip():
        raise ValueError("Result is empty")

    output_file = dist_path / "auto_annotated.conllu"
    output_file.write_text(result, encoding="utf-8")

    print(f"Done: {output_file}")


if __name__ == "__main__":
    main(Path(__file__).parent / "assets" / "articles", Path(__file__).parent / "dist")
