import gradio as gr
import shutil
import os
from pdf2norm import SmartPDFNormalizer

def process_pdf(pdf_file, insert_position):
    if not pdf_file:
        return None, None, None, "", "❌ Please upload a PDF file."

    out_dir = os.path.abspath("gradio_outputs")
    os.makedirs(out_dir, exist_ok=True)

    # Получаем базовое имя файла
    base_name = os.path.splitext(os.path.basename(pdf_file))[0]

    input_path = os.path.join(out_dir, f"{base_name}_input.pdf")
    output_path = os.path.join(out_dir, f"{base_name}_normalised.pdf")
    report_txt = os.path.join(out_dir, f"{base_name}_report.txt")
    report_json = os.path.join(out_dir, f"{base_name}_report.json")

    shutil.copy(pdf_file, input_path)

    normaliser = SmartPDFNormalizer(
        input_path=input_path,
        output_path=output_path,
        report_txt=report_txt,
        report_json=report_json,
        insert_blank_at=(insert_position - 1 if insert_position else None)
    )
    normaliser.normalize()

    with open(report_txt, "r", encoding="utf-8") as f:
        report_preview = f.read()

    return output_path, report_txt, report_json, report_preview, "✅ Normalisation completed successfully."


with gr.Blocks(title="SmartPDFNormalizer") as demo:
    gr.Markdown("# 📄 SmartPDFNormalizer\nNormalise PDF page sizes and optionally insert a blank page.")

    pdf_file = gr.File(label="Upload PDF", file_types=[".pdf"])
    insert_page = gr.Number(label="Insert blank page at (optional)", value=0, precision=0)
    run_button = gr.Button("Normalise PDF")

    output_pdf = gr.File(label="📄 Normalised PDF")
    output_txt = gr.File(label="📝 Text Report (.txt)")
    output_json = gr.File(label="🧾 JSON Report (.json)")
    report_preview = gr.Textbox(label="📋 Report Preview", lines=20)
    status_message = gr.Markdown()

    run_button.click(fn=process_pdf,
                     inputs=[pdf_file, insert_page],
                     outputs=[output_pdf, output_txt, output_json, report_preview, status_message])

demo.launch()
