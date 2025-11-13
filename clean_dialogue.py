import json
import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_dialogue(data):
    dialogue = []
    if isinstance(data, dict):
        if "role" in data and "text" in data:
            role = data["role"]
            text = data["text"]
            if not data.get("isThought", False):  # skip thinking process
                text = text.encode("utf-8").decode("unicode_escape").replace("\\n", "\n").strip()
                dialogue.append((role, text))
        for v in data.values():
            dialogue.extend(extract_dialogue(v))
    elif isinstance(data, list):
        for item in data:
            dialogue.extend(extract_dialogue(item))
    return dialogue


def clean_file(file_path):
    text = Path(file_path).read_text(encoding="utf-8", errors="ignore")

    # Fix trailing commas or partial JSON structure
    text = re.sub(r",\s*([}\]])", r"\1", text)

    try:
        data = json.loads(text)
    except Exception:
        # fallback: find the chunkedPrompt area only
        match = re.search(r'"chunks":\s*(\[.*\])\s*}', text, re.DOTALL)
        if not match:
            raise ValueError("Could not find valid JSON in file.")
        chunks_str = match.group(1)
        data = json.loads(f"[{chunks_str.strip('[]')}]")

    dialogue = extract_dialogue(data)

    cleaned_lines = []
    for role, msg in dialogue:
        role_tag = "user" if role.lower() == "user" else "ai"
        cleaned_lines.append(f"{role_tag}: {msg}")

    output = "\n\n".join(cleaned_lines)
    out_path = Path(file_path).parent / "Empathetic_Support_Full.txt"
    out_path.write_text(output, encoding="utf-8")
    return out_path


def main():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Select your Gemini export .txt file",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not path:
        return messagebox.showinfo("Cancelled", "No file selected.")

    try:
        out = clean_file(path)
        messagebox.showinfo("Done", f"✅ Cleaned chat saved as:\n{out}")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to process file:\n{e}")


if __name__ == "__main__":
    main()
