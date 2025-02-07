import os
import sys
from typing import Dict, List
import chess
from typing_extensions import Annotated

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from dotenv import load_dotenv
from openinference.instrumentation import using_prompt_template
from openinference.semconv.trace import SpanAttributes
from opentelemetry import trace, context
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from prompt_templates.router_template import SYSTEM_PROMPT
from skills.skill_map import SkillMap
from swarm import Agent, Swarm

load_dotenv()


class SwarmChessRouter:
    def __init__(self):
        self.client = Swarm()
        self.board = chess.Board()
        
        # Create white player agent with more explicit instructions
        self.white_player = Agent(
            name="White Player",
            instructions="""You are playing chess as White. On your turn:
            1. First call get_legal_moves() to see available moves
            2. Choose one of these legal moves
            3. Execute your chosen move using make_move(move)
            4. Moves should be in UCI format (e.g., 'e2e4', 'g1f3')
            Always make a move when it's your turn. Be decisive.""",
            functions=[
                self.get_legal_moves,
                self.make_move
            ]
        )
        
        # Create black player agent with more explicit instructions
        self.black_player = Agent(
            name="Black Player",
            instructions="""You are playing chess as Black. On your turn:
            1. First call get_legal_moves() to see available moves
            2. Choose one of these legal moves
            3. Execute your chosen move using make_move(move)
            4. Moves should be in UCI format (e.g., 'e7e5', 'b8c6')
            Always make a move when it's your turn. Be decisive.""",
            functions=[
                self.get_legal_moves,
                self.make_move
            ]
        )

    def get_legal_moves(self) -> str:
        """Returns a list of legal moves in UCI format"""
        moves = [str(move) for move in self.board.legal_moves]
        return f"Legal moves: {', '.join(moves)}"

    def make_move(self, move: str) -> str:
        """Execute a chess move in UCI format"""
        try:
            move_obj = chess.Move.from_uci(move)
            if move_obj in self.board.legal_moves:
                piece = self.board.piece_at(move_obj.from_square)
                piece_name = chess.piece_name(piece.piece_type).capitalize()
                self.board.push(move_obj)
                return f"Moved {piece_name} from {chess.square_name(move_obj.from_square)} to {chess.square_name(move_obj.to_square)}"
            else:
                return "Illegal move attempted"
        except Exception as e:
            return f"Error making move: {str(e)}"

    def process_query(self, query: str) -> str:
        current_player = self.white_player if self.board.turn else self.black_player
        player_color = "White" if self.board.turn else "Black"
        
        # Format board with code block for monospace display
        board_display = f"```\n{str(self.board)}\n```"
        
        message = {
            "role": "user",
            "content": f"""It's your turn as {player_color}.
Current board state:
{board_display}

Make your move by:
1. Check legal moves
2. Choose and execute a move
3. Explain your choice briefly"""
        }
        
        response = self.client.run(agent=current_player, messages=[message])
        
        if not response.messages:
            return f"Error: No response from {player_color} player"
        
        color_indicator = "🔵" if player_color == "White" else "🔴"
        final_response = f"{color_indicator} {player_color}'s turn:\n{response.messages[-1]['content']}"
        final_response += f"\n\nBoard after move:\n{board_display}"
        
        return final_response 