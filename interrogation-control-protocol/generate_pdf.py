"""
Generate a PDF of the README + Appendix (run output) for hackathon submission.
Uses fpdf2 — no system dependencies required.
"""
import os
import json
import re
from fpdf import FPDF

README_PATH = os.path.join(os.path.dirname(__file__), "README.md")
RESULTS_PATH = os.path.join(os.path.dirname(__file__), "results", "run_20260322_071016.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "Interrogation_Control_Protocol.pdf")

MARGIN = 18
LINE_HEIGHT = 6
COL_WIDTH = 174  # usable width at margin=18 on A4


class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Page {self.page_no()}", align="R")

    def chapter_title(self, text, level=1):
        if level == 1:
            self.set_font("Helvetica", "B", 16)
            self.set_text_color(10, 10, 10)
            self.multi_cell(COL_WIDTH, 9, text)
            self.set_draw_color(10, 10, 10)
            self.set_line_width(0.6)
            self.line(MARGIN, self.get_y(), MARGIN + COL_WIDTH, self.get_y())
            self.ln(4)
        elif level == 2:
            self.ln(4)
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(10, 10, 10)
            self.multi_cell(COL_WIDTH, 7, text)
            self.set_draw_color(180, 180, 180)
            self.set_line_width(0.3)
            self.line(MARGIN, self.get_y(), MARGIN + COL_WIDTH, self.get_y())
            self.ln(3)
        elif level == 3:
            self.ln(3)
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(30, 30, 30)
            self.multi_cell(COL_WIDTH, 6, text)
            self.ln(2)

    def body_text(self, text, indent=0):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.set_x(MARGIN + indent)
        self.multi_cell(COL_WIDTH - indent, LINE_HEIGHT, text)

    def bullet(self, label, text, indent=4):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 30, 30)
        self.set_x(MARGIN + indent)
        # Write label inline then continue with text
        label_w = self.get_string_width(label + "  ")
        self.cell(label_w, LINE_HEIGHT, label)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(COL_WIDTH - indent - label_w, LINE_HEIGHT, text)

    def numbered_item(self, number, label, text, indent=4):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 30, 30)
        self.set_x(MARGIN + indent)
        prefix = f"{number}. {label}"
        prefix_w = self.get_string_width(prefix + "  ")
        self.cell(prefix_w, LINE_HEIGHT, prefix)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(COL_WIDTH - indent - prefix_w, LINE_HEIGHT, text)

    def code_block(self, text):
        self.set_font("Courier", "", 8.5)
        self.set_fill_color(244, 244, 244)
        self.set_text_color(30, 30, 30)
        self.set_x(MARGIN)
        self.multi_cell(COL_WIDTH, 5, text, fill=True)
        self.ln(2)

    def subtitle(self, text):
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(90, 90, 90)
        self.multi_cell(COL_WIDTH, 6, text)
        self.ln(4)


def strip_md_inline(text):
    """Strip basic inline markdown: **bold**, `code`, expand [text](url) to text (url)"""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1 (\2)', text)
    # Replace unicode chars not in latin-1
    text = text.replace('\u2014', '--').replace('\u2013', '-').replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    return text


def strip_bold_code(text):
    """Strip **bold** and `code` only — leave links intact for clickable rendering."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    return sanitize(text)


def write_with_links(pdf, text, h=6, indent=0):
    """Render a text segment inline, making [label](url) patterns clickable."""
    parts = re.split(r'(\[.+?\]\(.+?\))', text)
    pdf.set_x(MARGIN + indent)
    for part in parts:
        m = re.match(r'\[(.+?)\]\((.+?)\)', part)
        if m:
            label = sanitize(m.group(1))
            url = m.group(2)
            pdf.set_text_color(30, 80, 180)
            pdf.set_font("Helvetica", "U", 10)
            pdf.write(h, label, link=url)
            pdf.set_text_color(30, 30, 30)
            pdf.set_font("Helvetica", "", 10)
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 30, 30)
            pdf.write(h, strip_bold_code(part))
    pdf.ln(h)


def parse_and_render(pdf, md_text):
    """Parse markdown line by line and render to PDF."""
    lines = md_text.split("\n")
    in_code_block = False
    code_buffer = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith("```"):
            if in_code_block:
                pdf.code_block("\n".join(code_buffer))
                code_buffer = []
                in_code_block = False
            else:
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        # Headings
        if line.startswith("### "):
            pdf.chapter_title(strip_md_inline(line[4:]), level=3)
        elif line.startswith("## "):
            pdf.chapter_title(strip_md_inline(line[3:]), level=2)
        elif line.startswith("# "):
            pdf.chapter_title(strip_md_inline(line[2:]), level=1)

        # Markdown table — collect all rows
        elif line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r'^\|[-| :]+\|$', lines[i]):
                    table_lines.append(lines[i])
                i += 1
            render_table(pdf, table_lines)
            continue

        # Bullet points
        elif line.startswith("- "):
            content = strip_md_inline(line[2:])
            # Check for bold label pattern: **label** — rest
            m = re.match(r'\*\*(.+?)\*\*\s*[—-]\s*(.*)', line[2:])
            if m:
                pdf.bullet(sanitize(m.group(1)) + " --", sanitize(m.group(2)))
            else:
                pdf.bullet("•", content)

        # Numbered list
        elif re.match(r'^\d+\. ', line):
            m = re.match(r'^(\d+)\. (.*)', line)
            num = m.group(1)
            rest = m.group(2)
            bm = re.match(r'\*\*(.+?)\*\*\s*[—-]\s*(.*)', rest)
            if bm:
                label = sanitize(bm.group(1)) + " --"
                body = bm.group(2)
                if re.search(r'\[.+?\]\(.+?\)', body):
                    # Render prefix with cell, then body with clickable links
                    pdf.set_font("Helvetica", "B", 10)
                    pdf.set_text_color(30, 30, 30)
                    pdf.set_x(MARGIN + 4)
                    prefix = f"{num}. {label} "
                    prefix_w = pdf.get_string_width(prefix)
                    pdf.cell(prefix_w, LINE_HEIGHT, prefix)
                    # write_with_links continues inline from current x
                    parts = re.split(r'(\[.+?\]\(.+?\))', body)
                    for part in parts:
                        lm = re.match(r'\[(.+?)\]\((.+?)\)', part)
                        if lm:
                            link_label = sanitize(lm.group(1))
                            url = lm.group(2)
                            pdf.set_text_color(30, 80, 180)
                            pdf.set_font("Helvetica", "U", 10)
                            pdf.write(LINE_HEIGHT, link_label, link=url)
                            pdf.set_text_color(30, 30, 30)
                            pdf.set_font("Helvetica", "", 10)
                        else:
                            pdf.set_font("Helvetica", "", 10)
                            pdf.set_text_color(30, 30, 30)
                            pdf.write(LINE_HEIGHT, strip_bold_code(part))
                    pdf.ln(LINE_HEIGHT)
                else:
                    pdf.numbered_item(num, label, strip_md_inline(body))
            else:
                pdf.numbered_item(num, "", strip_md_inline(rest))

        # Blank line
        elif line.strip() == "":
            pdf.ln(3)

        # Normal paragraph text
        else:
            if re.search(r'\[.+?\]\(.+?\)', line):
                write_with_links(pdf, line)
            else:
                pdf.body_text(strip_md_inline(line))

        i += 1


def render_table(pdf, table_lines):
    if not table_lines:
        return

    headers = [c.strip() for c in table_lines[0].split("|") if c.strip()]
    n = len(headers)
    col_w = COL_WIDTH / n

    # Header row
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(26, 26, 26)
    pdf.set_text_color(255, 255, 255)
    pdf.set_x(MARGIN)
    for h in headers:
        pdf.cell(col_w, 6, h[:20], border=0, fill=True)
    pdf.ln()

    # Data rows
    for idx, row_line in enumerate(table_lines[1:]):
        cells = [c.strip() for c in row_line.split("|") if c.strip()]
        fill = idx % 2 == 0
        pdf.set_fill_color(249, 249, 249) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(30, 30, 30)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_x(MARGIN)
        for ci, cell in enumerate(cells[:n]):
            pdf.cell(col_w, 5.5, strip_md_inline(cell)[:25], border=0, fill=fill)
        pdf.ln()
    pdf.ln(3)


def build_appendix(pdf, results_path):
    with open(results_path) as f:
        results = json.load(f)

    pdf.add_page()
    pdf.chapter_title("Appendix -- Full Run Output", level=1)
    pdf.subtitle("run_20260322_071016  |  8 scenarios x 3 conditions = 24 evaluations")

    pdf.body_text(
        "The table below contains all 24 evaluations from the run used to produce the results "
        "reported in this submission. Each row shows the scenario, condition, classifier decision, "
        "safety and usefulness scores, whether the decision was correct, and the classifier's reasoning."
    )
    pdf.ln(4)

    headers = ["ID", "Condition", "Description", "Malicious", "Decision", "Safety", "Useful", "Correct", "Reasoning"]
    col_widths = [8, 18, 32, 16, 16, 12, 12, 14, 46]

    # Header
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_fill_color(26, 26, 26)
    pdf.set_text_color(255, 255, 255)
    pdf.set_x(MARGIN)
    for h, w in zip(headers, col_widths):
        pdf.cell(w, 6, h, border=0, fill=True)
    pdf.ln()

    for idx, r in enumerate(results):
        fill = idx % 2 == 0
        pdf.set_fill_color(249, 249, 249) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(30, 30, 30)
        pdf.set_x(MARGIN)

        decision_color = (192, 57, 43) if r["decision"] == "BLOCK" else (39, 174, 96)
        correct_mark = "Yes" if r["correct"] else "No"
        correct_color = (39, 174, 96) if r["correct"] else (192, 57, 43)
        reasoning_short = sanitize(r["reasoning"])
        reasoning_short = reasoning_short[:80] + "..." if len(reasoning_short) > 80 else reasoning_short

        values = [
            sanitize(r["scenario_id"]),
            sanitize(r["condition"].upper()),
            sanitize(r["description"][:28]),
            "Yes" if r["malicious_intent"] else "No",
            sanitize(r["decision"]),
            f"{r['safety_score']:.2f}",
            f"{r['usefulness_score']:.2f}",
            correct_mark,
            reasoning_short,
        ]
        colors = [None, None, None, None, decision_color, None, None, correct_color, None]

        for val, w, col in zip(values, col_widths, colors):
            if col:
                pdf.set_text_color(*col)
                pdf.set_font("Helvetica", "B", 7)
            else:
                pdf.set_text_color(30, 30, 30)
                pdf.set_font("Helvetica", "", 7)
            pdf.cell(w, 5, val, border=0, fill=fill)
        pdf.ln()

    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.set_x(MARGIN)
    pdf.multi_cell(COL_WIDTH, 5,
        "Note: Reasoning strings are truncated to 80 characters for display. "
        "Full reasoning for all 24 evaluations is available in "
        "results/run_20260322_071016.json in the project repository.")
    pdf.ln(6)
    pdf.chapter_title("Summary", level=2)

    summary_headers = ["Condition", "Scenarios", "Correct", "Accuracy", "Avg Safety", "Avg Usefulness", "False Pos", "False Neg"]
    summary_rows = [
        ["BASELINE", "8", "4", "50.0%", "0.96", "0.91", "0", "4"],
        ["UNAWARE",  "8", "3", "37.5%", "0.61", "0.53", "2", "3"],
        ["AWARE",    "8", "6", "75.0%", "0.67", "0.54", "0", "2"],
    ]
    sw = COL_WIDTH / len(summary_headers)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(26, 26, 26)
    pdf.set_text_color(255, 255, 255)
    pdf.set_x(MARGIN)
    for h in summary_headers:
        pdf.cell(sw, 6, h, border=0, fill=True)
    pdf.ln()

    for idx, row in enumerate(summary_rows):
        bold = row[0] == "AWARE"
        fill = idx % 2 == 0
        pdf.set_fill_color(249, 249, 249) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Helvetica", "B" if bold else "", 8)
        pdf.set_text_color(30, 30, 30)
        pdf.set_x(MARGIN)
        for cell in row:
            pdf.cell(sw, 5.5, cell, border=0, fill=fill)
        pdf.ln()


def sanitize(text):
    return text.replace('\u2014', '--').replace('\u2013', '-').replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"').replace('\u2022', '*').replace('\u2026', '...')


def main():
    print("Reading README...")
    with open(README_PATH) as f:
        md_text = f.read()
    md_text = sanitize(md_text)

    # Split title, subtitle, body
    lines = md_text.split("\n")
    title = lines[0].lstrip("# ").strip()
    subtitle_text = lines[2].strip() if len(lines) > 2 else ""
    body = "\n".join(lines[3:])

    pdf = PDF()
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()

    # Title block
    pdf.ln(4)
    pdf.chapter_title(title, level=1)
    if subtitle_text:
        pdf.subtitle(subtitle_text)

    print("Rendering README body...")
    parse_and_render(pdf, body)

    print("Building appendix...")
    build_appendix(pdf, RESULTS_PATH)

    print(f"Saving PDF to {OUTPUT_PATH}...")
    pdf.output(OUTPUT_PATH)
    print(f"Done. PDF saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
