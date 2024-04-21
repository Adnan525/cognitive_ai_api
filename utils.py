def render_move_text(moves: str):
    if moves == "":
        return "No moves yet"
    moves_list = moves.split()
    side = "White" if len(moves_list) % 2 == 1 else "Black"
    prevs = "\n"
    for i, move in enumerate(moves_list[:-1]):
        prevs += f"{move} "
        if (i + 1) % 2 == 0:
            prevs += "\n"
    return f"Current move : {side, moves_list[-1]} \nPrevious moves : {prevs}"

def generate_prompt(moves:str):
    temp = moves.strip()
    prev = temp[:-4]
    if(len(temp) <= 4):
        prev = "NONE"

    return f"In a paragraph, explain the rationale behind the last move, where all previous moves are - previous moves : {prev}, last move : {temp[-4:]}."

# print(generate_prompt("Nf3 "))