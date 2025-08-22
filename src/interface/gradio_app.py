"""
Gradio interface for the tennis booking assistant.
"""

import os
import gradio as gr
from typing import List, Tuple

from ..agent.tennis_agent import TennisBookingAgent


class TennisBookingInterface:
    """Gradio interface for the tennis booking assistant."""
    
    def __init__(self, openai_api_key: str):
        self.agent = TennisBookingAgent(openai_api_key)
        self.chat_history: List[Tuple[str, str]] = []
    
    def chat_with_agent(self, message: str, history: List[List[str]]) -> Tuple[str, List[List[str]]]:
        """
        Process a chat message and return the agent's response.
        
        Args:
            message: User's message
            history: Chat history
            
        Returns:
            Tuple of (response, updated_history)
        """
        if not message.strip():
            return "", history
        
        # Process the message with the agent
        response = self.agent.process_request(message)
        
        # Update history
        history.append([message, response])
        
        return "", history
    
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
            """
        ) as interface:
            
            gr.Markdown("""
            # 🎾 Tennis Buchungsassistent
            
            **Sport- und Tennis-Club München Süd**
            
            Frag mich, um dir bei der Suche und Buchung von Tennisplätzen zu helfen! Ich kann die Verfügbarkeit prüfen und basierend auf deinen Vorlieben die besten Optionen vorschlagen.
            
            **Beispielanfragen:**
            - "Ich möchte morgen um 15 Uhr Tennis spielen"
            - "Mein Name ist John, ich bevorzuge Sandplätze"
            - "Suche nach Hallenplätzen für Einzel am Freitag"
            - "Brauche einen Platz für Doppel am Wochenende"
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Chat interface
                    chatbot = gr.Chatbot(
                        label="Chat mit Tennis Assistent",
                        height=500,
                        show_label=True,
                        container=True,
                        bubble_full_width=False
                    )
                    
                    with gr.Row():
                        # Text input
                        msg = gr.Textbox(
                            label="Nachricht eingeben",
                            placeholder="z.B., Ich möchte morgen um 15 Uhr Tennis spielen",
                            lines=2,
                            scale=3
                        )
                        
                        # Voice input
                        voice_input = gr.Audio(
                            label="Spracheingabe",
                            type="microphone",
                            scale=1
                        )
                    
                    with gr.Row():
                        submit_btn = gr.Button("Senden", variant="primary", size="lg")
                        clear_btn = gr.Button("Chat löschen", variant="secondary")
                
                with gr.Column(scale=1):
                    # Information panel
                    gr.Markdown("""
                    ### 📋 Verfügbare Plätze
                    
                    **Links (Tennisschule):**
                    - Platz A: Aufschlagtrainingsplatz (nur Einzel)
                    - Platz 1-6: Tennisschule (Platz 1-5 sind Mittelplätze)
                    
                    **Eingang rechts:**
                    - Platz 7-9: Sandplätze (Platz 8 ist Mittelplatz)
                    - Platz 10-12: Granulatplätze (Platz 11 ist Mittelplatz)
                    
                    **Mitte:**
                    - T-Platz: vor dem Restaurant (nur Einzel)
                    
                    **Hinten:**
                    - Platz 14-22: Sandplätze (Platz 15, 18, 21 sind Mittelplätze)
                    - Platz 17: Wingfield
                    
                    ### 🎯 Tipps
                    - Sei spezifisch bei Datum und Uhrzeit
                    - Erwähne Platztyp-Vorlieben
                    - Gib an ob Einzel oder Doppel
                    """)
                    
                    # Quick action buttons
                    gr.Markdown("### ⚡ Schnellaktionen")
                    
                    with gr.Row():
                        today_btn = gr.Button("Heute", size="sm")
                        tomorrow_btn = gr.Button("Morgen", size="sm")
                    
                    with gr.Row():
                        clay_btn = gr.Button("Sandplätze", size="sm")
            
            # Event handlers
            submit_btn.click(
                self.chat_with_agent,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )
            
            msg.submit(
                self.chat_with_agent,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )
            
            clear_btn.click(
                lambda: ([], ""),
                outputs=[chatbot, msg]
            )
            
            # Quick action buttons
            today_btn.click(
                lambda: ("Ich möchte heute Tennis spielen", []),
                outputs=[msg, chatbot]
            )
            
            tomorrow_btn.click(
                lambda: ("Ich möchte morgen Tennis spielen", []),
                outputs=[msg, chatbot]
            )
            
            clay_btn.click(
                lambda: ("Ich bevorzuge Sandplätze", []),
                outputs=[msg, chatbot]
            )
            

            
            # Voice input processing (placeholder - would need speech-to-text)
            def process_voice(audio):
                if audio is None:
                    return ""
                # In a real implementation, you would use speech-to-text here
                return "Spracheingabe empfangen (Sprach-zu-Text nicht implementiert)"
            
            voice_input.change(
                process_voice,
                inputs=[voice_input],
                outputs=[msg]
            )
        
        return interface


def create_app(openai_api_key: str) -> gr.Blocks:
    """Create and return the Gradio app."""
    interface = TennisBookingInterface(openai_api_key)
    return interface.create_interface()


if __name__ == "__main__":
    # For testing - you would normally get this from environment
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    app = create_app(api_key)
    app.launch(share=True)
