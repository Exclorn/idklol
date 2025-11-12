from pathlib import Path
import json
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def clean_file(file_path):
    raw_text = Path(file_path).read_text(encoding="utf-8", errors="ignore")

    # 🧹 Extract all "text": "...", and their associated "role"
    # Convert JSON-like text into something readable
    pattern = re.compile(r'"role":\s*"(\w+)"\s*,\s*"tokenCount":\s*\d+\s*},?\s*{\s*"text":\s*"([^"]*?)"', re.DOTALL)
    matches = pattern.findall(raw_text)

    dialogue_lines = []

    for role, text in matches:
        text = text.encode("utf-8").decode("unicode_escape")  # decode \u codes
        text = text.replace("\\n", "\n").strip()
        if not text:
            continue

        if role.lower() == "user":
            dialogue_lines.append(f"user: {text}")
        elif role.lower() == "model":
            # Remove thinking process segments
            text = re.sub(r"Thinking Process:.*?(?=\n\S|$)", "", text, flags=re.DOTALL).strip()
            dialogue_lines.append(f"ai: {text}")

    # Join messages cleanly with line breaks
    cleaned_dialogue = "\n\n".join(dialogue_lines)

    # Save cleaned output
    output_path = Path(file_path).parent / "Empathetic_Support_Full.txt"
    output_path.write_text(cleaned_dialogue, encoding="utf-8")

    return output_path


def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select your 'Empathetic Support for Loneliness.txt' file",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not file_path:
        messagebox.showinfo("Cancelled", "No file selected.")
        return

    output = clean_file(file_path)
    messagebox.showinfo("Success", f"✅ Cleaned conversation saved as:\n{output}")


if __name__ == "__main__":
    main()
