#pdf2norm.py
import json
import fitz
import argparse
from collections import Counter
import os


class SmartPDFNormalizer:
    def __init__(self, input_path, output_path, report_txt="report.txt", report_json="report.json",
                 insert_blank_at=None):
        self.input_path = input_path
        self.output_path = output_path
        self.report_txt = report_txt
        self.report_json = report_json
        self.insert_blank_at = insert_blank_at  # Optional: position to insert blank page (0-based index)
        self.page_sizes = []
        self.report = []

    def _round_size(self, w, h, precision=2):
        return (round(w, precision), round(h, precision))

    def _get_mode_size(self, sizes):
        rounded = [self._round_size(w, h) for w, h in sizes]
        most_common = Counter(rounded).most_common(1)[0][0]
        return most_common

    def _get_average_similar_sizes(self, sizes, mode_size, tolerance=0.15):
        similar = [
            (w, h) for (w, h) in sizes
            if abs(w - mode_size[0]) <= tolerance and abs(h - mode_size[1]) <= tolerance
        ]
        avg_width = sum(w for w, _ in similar) / len(similar)
        avg_height = sum(h for _, h in similar) / len(similar)
        return round(avg_width, 2), round(avg_height, 2)

    def normalize(self):
        src_doc = fitz.open(self.input_path)
        dst_doc = fitz.open()

        self.page_sizes = [(p.rect.width, p.rect.height) for p in src_doc]

        # Step 1: find mode size
        mode_size = self._get_mode_size(self.page_sizes)

        # Step 2: get average of similar sizes
        target_width, target_height = self._get_average_similar_sizes(
            self.page_sizes, mode_size
        )
        ref_rect = fitz.Rect(0, 0, target_width, target_height)

        page_offset = 0
        for i, page in enumerate(src_doc):
            current_page_index = i + page_offset
            if self.insert_blank_at is not None and current_page_index == self.insert_blank_at:
                dst_doc.new_page(pno=current_page_index, width=target_width, height=target_height)
                self.report.append({
                    "page": current_page_index + 1,
                    "original_width": round(target_width, 2),
                    "original_height": round(target_height, 2),
                    "status": "blank_inserted"
                })
                page_offset += 1

            w, h = page.rect.width, page.rect.height
            if abs(w - target_width) <= 0.15 and abs(h - target_height) <= 0.15:
                matrix = fitz.Matrix(1, 1)
                status = "unchanged"
            else:
                matrix = fitz.Matrix(target_width / w, target_height / h)
                status = "resized"

            dst_page = dst_doc.new_page(width=target_width, height=target_height)
            dst_page.show_pdf_page(ref_rect, src_doc, i, matrix)
            self.report.append({
                "page": current_page_index + 1 + (1 if self.insert_blank_at is not None and current_page_index >= self.insert_blank_at else 0),
                "original_width": round(w, 2),
                "original_height": round(h, 2),
                "status": status
            })

        dst_doc.save(self.output_path)
        dst_doc.close()

        self._save_report_txt()
        self._save_report_json()

    def _save_report_txt(self):
        with open(self.report_txt, "w", encoding="utf-8") as f:
            f.write("Report of changes:\n\n")
            for entry in self.report:
                f.write(
                    f"Page {entry['page']:>3}: "
                    f"{entry['original_width']} x {entry['original_height']} → {entry['status']}\n"
                )

    def _save_report_json(self):
        with open(self.report_json, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Normalisation of PDF page sizes and insertion of a blank page.")
    parser.add_argument("input", help="Path to the source PDF file.")
    parser.add_argument("output", help="Path to the output PDF file.")
    parser.add_argument("--insert_blank", type=int, help="Page number (starting from 1) at which to insert a blank page.")
    parser.add_argument("--report_txt", default="report.txt", help="Path to the text report file.")
    parser.add_argument("--report_json", default="report.json", help="Path to the JSON report file.")

    args = parser.parse_args()

    insert_index = args.insert_blank - 1 if args.insert_blank else None

    normalizer = SmartPDFNormalizer(
        input_path=args.input,
        output_path=args.output,
        report_txt=args.report_txt,
        report_json=args.report_json,
        insert_blank_at=insert_index
    )
    normalizer.normalize()


if __name__ == "__main__":
    main()


