import gradio as gr
from generate import generate_answer

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    
    result = generate_answer(question)
    
    sources = "\n".join([f"• {s}" for s in result["sources"]])
    
    return result["answer"], sources

with gr.Blocks(title="The Unofficial Guide - BC CS Professors") as demo:
    gr.Markdown("# 🎓 The Unofficial Guide")
    gr.Markdown("Ask questions about CS professors at Brooklyn College based on real student reviews.")
    
    with gr.Row():
        inp = gr.Textbox(
            label="Your question",
            placeholder="e.g. Is Moshe Lach good for beginners?",
            lines=2
        )
    
    btn = gr.Button("Ask", variant="primary")
    
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()