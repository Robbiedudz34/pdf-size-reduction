import subprocess
from pathlib import Path

# Ghostscript must be installed and added to system PATH for this to work
def compress_pdf_with_ghostscript(input_path, target_preset="/ebook"):
    """
    Compress a PDF using Ghostscript.
    target_preset options: /screen, /ebook, /printer, /prepress
    Output saved in script directory as reduced_{stem}.pdf
    """
    # Use a valid file path and verify it is a PDF
    input_path = Path(input_path).resolve()
    if not input_path.exists() or input_path.suffix.lower() != ".pdf":
        print("Provide a valid PDF")
        return

    output_path = Path.cwd() / f"reduced_{input_path.stem}.pdf"
    input_size = input_path.stat().st_size / 1_000_000
    print(f"Original file: {input_path.name}")
    print(f"Original size: {input_size:.2f} MB\n")

    # Ghostscript command
    cmd = [
        "gswin64c",                        # Windows Ghostscript executable
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={target_preset}",  # /screen, /ebook, /printer, /prepress
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        str(input_path),
    ]

    try:
        subprocess.run(cmd, check=True)
        new_size = output_path.stat().st_size / 1_000_000
        print(f"Compressed size: {new_size:.2f} MB")
        print(f"Saved as: {output_path}")
    except subprocess.CalledProcessError:
        print("Ghostscript encountered an error while compressing the file.")

if __name__ == "__main__":
    print("Drag and drop your PDF file here, or paste full path:")
    user_input = input(">> ").strip().strip('"')
    if user_input:
        compress_pdf_with_ghostscript(user_input, target_preset="/ebook")
