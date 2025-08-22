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
            title="Tennis Booking Assistant",
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
            # 🎾 Tennis Booking Assistant
            
            **Sport- und Tennis-Club München Süd**
            
            Ask me to help you find and book tennis courts! I can check availability and suggest the best options based on your preferences.
            
            **Example requests:**
            - "I want to play tennis tomorrow at 3pm"
            - "My name is John, I prefer clay courts"
            - "Looking for indoor courts for singles on Friday"
            - "Need a court for doubles this weekend"
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Chat interface
                    chatbot = gr.Chatbot(
                        label="Chat with Tennis Assistant",
                        height=500,
                        show_label=True,
                        container=True,
                        bubble_full_width=False
                    )
                    
                    with gr.Row():
                        # Text input
                        msg = gr.Textbox(
                            label="Type your message",
                            placeholder="e.g., I want to play tennis tomorrow at 3pm",
                            lines=2,
                            scale=3
                        )
                        
                        # Voice input
                        voice_input = gr.Audio(
                            label="Voice Input",
                            type="microphone",
                            scale=1
                        )
                    
                    with gr.Row():
                        submit_btn = gr.Button("Send", variant="primary", size="lg")
                        clear_btn = gr.Button("Clear Chat", variant="secondary")
                
                with gr.Column(scale=1):
                    # Information panel
                    gr.Markdown("""
                    ### 📋 Available Courts
                    
                    **Main Building (Clay):**
                    - Platz A, Platz 1-9
                    - Platz 2 is a middle court
                    
                    **Outdoor Courts:**
                    - Platz 10-12 (Granulat)
                    - Platz 14-22 (Hard)
                    - Platz 17 (Wingfield)
                    
                    **Indoor:**
                    - T-Platz (Singles only)
                    
                    ### 🎯 Tips
                    - Be specific about date and time
                    - Mention court type preferences
                    - Specify singles or doubles
                    - I'll remember your preferences!
                    """)
                    
                    # Quick action buttons
                    gr.Markdown("### ⚡ Quick Actions")
                    
                    with gr.Row():
                        today_btn = gr.Button("Today", size="sm")
                        tomorrow_btn = gr.Button("Tomorrow", size="sm")
                    
                    with gr.Row():
                        clay_btn = gr.Button("Clay Courts", size="sm")
                        indoor_btn = gr.Button("Indoor", size="sm")
            
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
                lambda: ("I want to play tennis today", []),
                outputs=[msg, chatbot]
            )
            
            tomorrow_btn.click(
                lambda: ("I want to play tennis tomorrow", []),
                outputs=[msg, chatbot]
            )
            
            clay_btn.click(
                lambda: ("I prefer clay courts", []),
                outputs=[msg, chatbot]
            )
            
            indoor_btn.click(
                lambda: ("I want an indoor court", []),
                outputs=[msg, chatbot]
            )
            
            # Voice input processing (placeholder - would need speech-to-text)
            def process_voice(audio):
                if audio is None:
                    return ""
                # In a real implementation, you would use speech-to-text here
                return "Voice input received (speech-to-text not implemented)"
            
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
