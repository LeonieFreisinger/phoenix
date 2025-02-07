import os
import sys
import logging

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import gradio as gr
from router import SwarmChessRouter
from utils.instrument import Framework, instrument

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def chess_game():
    """Run an autonomous chess game"""
    logger.info("Starting new chess game")
    router = SwarmChessRouter()
    chat_history = []
    
    # Initial board state
    initial_state = f"Initial board state:\n```\n{str(router.board)}\n```"
    logger.info(f"Game initialized:\n{initial_state}")
    chat_history.append(("Game Start", initial_state))
    yield chat_history
    
    # Start the game
    move_count = 0
    while not router.board.is_game_over():
        current_player = "White" if router.board.turn else "Black"
        message = f"It's {current_player}'s turn."
        logger.info(f"Move {move_count + 1}: {message}")
        
        try:
            response = router.process_query(message)
            logger.info(f"Response received: {response}")
            chat_history.append((message, response))
            move_count += 1
            yield chat_history
        except Exception as e:
            logger.error(f"Error processing move: {str(e)}")
            break
    
    # Add game over message
    if router.board.is_checkmate():
        winner = "Black" if router.board.turn else "White"
        final_msg = f"{winner} wins by checkmate!\n\nFinal board state:\n```\n{str(router.board)}\n```"
    elif router.board.is_stalemate():
        final_msg = f"Draw by stalemate!\n\nFinal board state:\n```\n{str(router.board)}\n```"
    else:
        final_msg = f"Game ended unexpectedly.\n\nFinal board state:\n```\n{str(router.board)}\n```"
    
    logger.info(f"Game over: {final_msg}")
    chat_history.append(("Game Over", final_msg))
    yield chat_history

def launch_app():
    with gr.Blocks(title="OpenAI Swarms Chess Agent - Autonomous Chess Game", css="""
        .white-player {
            background-color: #f0f0f0 !important;
        }
        .black-player {
            background-color: #e0e0e0 !important;
        }
        code {
            font-family: "Courier New", Courier, monospace !important;
            white-space: pre !important;
            display: block !important;
            padding: 10px !important;
            background-color: white !important;
            border-radius: 5px !important;
            font-size: 14px !important;
            line-height: 1.2 !important;
        }
    """) as iface:
        gr.Markdown("# ♟️ Autonomous Chess Game")
        chatbot = gr.Chatbot(
            height=800,
            elem_classes=["chess-chat"],
            render=lambda x: {
                "visible": True,
                "value": x,
                "elem_classes": ["white-player" if "White's turn" in x[0] else "black-player" if "Black's turn" in x[0] else ""]
            }
        )
        
        start_btn = gr.Button("Start New Game", variant="primary")
        
        start_btn.click(
            fn=chess_game,
            outputs=[chatbot],
        )

    iface.queue()
    iface.launch()

if __name__ == "__main__":
    launch_app() 