from src.game import Game
import cv2

if __name__ == "__main__":

    game = Game("Bitburner")
    game.focus_game_window()
    state = game.capture_state()
