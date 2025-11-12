from pathlib import Path
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def clean_file(file_path):
    text = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    cleaned_text = re.sub(r"Thinking Process:.*?(?=\n\S|$)", "", text, flags=re.DOTALL)
    dialogue_lines = []

    for line in cleaned_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(("user:", "model:")) or (
            not line.lower().startswith(("system", "draft", "final", "here’s", "{", "}", "["))
            and not re.match(r"^tokenCount", line)
        ):
            dialogue_lines.append(line)

    formatted_dialogue = []
    for line in dialogue_lines:
        if line.startswith("model:"):
            formatted_dialogue.append("ai:" + line[len("model:"):].strip())
        elif line.startswith("user:"):
            formatted_dialogue.append("user:" + line[len("user:"):].strip())
        else:
            if re.match(r"^(i |why|how|it|okay|ah|kinda|really|are|mai|ewa|nas)", line, re.I):
                formatted_dialogue.append("user: " + line)
            else:
                formatted_dialogue.append("ai: " + line)

    cleaned_dialogue = "\n\n".join(formatted_dialogue)
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
    messagebox.showinfo("Success", f"✅ Cleaned file saved as:\n{output}")

if __name__ == "__main__":
    main()
