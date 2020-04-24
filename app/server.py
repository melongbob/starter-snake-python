import json
import os
import random

import bottle
from bottle import HTTPResponse


@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    response = {"color": "#F4C2C2", "headType": "bendr", "tailType": "curled"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json

    # Choose a random direction to move in
    moves = ["up", "down", "right", "left"]

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "I am Curly the snake!"

    head = data["you"]["body"][0]
    health = data["you"]["health"]
    board = data["board"]
    snakes = data["board"]["snakes"]
    food = data["board"]["food"][0]

    for _ in range(10):
        if health > 20:
            move = random.choice(moves)
        else:
            move = moves[data["turn"]%4]
        coord = moveAsCoord(move, head)
        if isValidMove(move, head, board, coord, snakes):
            break
            
    response = {"move": move, "shout": shout}        

    print("MOVE:", json.dumps(data))

    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )

def moveAsCoord(move, head):
    if move == "up":
        return {"x": head["x"], "y": head["y"] - 1}
    elif move == "down":
        return {"x": head["x"], "y": head["y"] + 1}
    elif move == "right":
        return {"x": head["x"] + 1, "y": head["y"]}
    elif move == "left":
        return {"x": head["x"] - 1, "y": head["y"]}

def isValidMove(move, head, board, coord, snakes):
    if not isOffBoard(board, coord) and not isSnake(coord, snakes):
        return True
    else:
        return False

def isOffBoard(board, coord):
    if coord["x"] < 0: return True
    if coord["y"] < 0: return True
    if coord["y"] >= board["height"]: return True
    if coord["x"] >= board["width"]: return True
    return False

def isSnake(coord, snakes):
    for snake in snakes:
        if coord in snake["body"]:
            return True
    return False

@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
