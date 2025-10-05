"""
Gradio interface for the tennis booking assistant.
"""

import os
import gradio as gr

from src.interface.agent import BookingManager


class TennisBookingInterface:
    """Gradio interface for the tennis booking assistant."""

    def __init__(self, openai_api_key: str, openai_model: str):
        self.agent = BookingManager(openai_api_key, openai_model)
        self.chat_history: list[dict] = []

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface."""
        with gr.Blocks(
            title="Tennis Buchungsassistent",
            theme=gr.themes.Soft(),
            css="""
            .chat-container {
                max-height: 600px;
                overflow-y: auto;
            }
            .response-container {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                border-left: 4px solid #007bff;
            }
            """,
        ) as interface:

            gr.Markdown(
                """
            # 🎾 Tennis Buchungsassistent
            
            Frag mich, um dir bei der Suche von freien Tennisplätzen beim STC München zu helfen! Ich kann die Verfügbarkeit prüfen und basierend auf deinen Vorlieben die besten Optionen vorschlagen.
            
            **Beispielanfragen:**
            - "Ich möchte morgen um 15 Uhr Tennis spielen"
            - "Mein Name ist John, ich bevorzuge Sandplätze"
            - "Suche nach Hallenplätzen für Einzel am Freitag"
            - "Brauche einen Platz für Doppel am Wochenende"
            """
            )

            # Chat interface
            chatbot = gr.Chatbot(
                label="Chat mit Tennis Assistent",
                height=500,
                show_label=True,
                container=True,
                type="messages",
            )

            with gr.Row():
                # Text input
                msg = gr.Textbox(
                    label="Nachricht eingeben",
                    placeholder="z.B., Ich möchte morgen um 15 Uhr Tennis spielen",
                    lines=2,
                    scale=3,
                )

            with gr.Row():
                submit_btn = gr.Button("Senden", variant="primary", size="lg")
                clear_btn = gr.Button("Chat löschen", variant="secondary")

            # Event handlers
            submit_btn.click(
                self.agent.run,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot],
            )

            msg.submit(
                self.agent.run,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot],
            )

            clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg])

        return interface


def create_app(openai_api_key: str, openai_model: str) -> gr.Blocks:
    """Create and return the Gradio app."""
    interface = TennisBookingInterface(openai_api_key, openai_model)
    return interface.create_interface()


if __name__ == "__main__":
    # For testing - you would normally get this from environment
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    openai_model = os.getenv("OPENAI_MODEL_NAME", "your-api-key-here")
    app = create_app(api_key, openai_model)
    app.launch(share=True)
