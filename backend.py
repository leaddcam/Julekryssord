from flask import Flask, render_template, request, redirect, url_for, jsonify

backend = Flask(__name__)
backend.secret_key = "hemmelig"

# Make `enumerate` available in Jinja2 templates
backend.jinja_env.globals.update(enumerate=enumerate)
# crossword data
crossword_data = {
    'size': 11,
    'grid': [
            [True, True, True, True, True, False, False, False, False, False, False], # vaule 5 6 7 8 9 10
            [True, False, False, False, False, False, False, False, False, False, False], # e 1 2 3 4 5 6 7 8 9 10
            [True, False, True, True, True, True, True, True, True, True, True], # s 1 musically
            [True, True, True, False, True, False, False, False, False, False, False], # tea 3 w 5 6 7 8 9 10
            [False, False, True, False, True, False, False, False, False, False, False], # 0 1 p 3 e 5 6 7 8 9 10
            [False, False, True, False, True, False, False, False, False, False, False], # 0 1 s 3 e 5 6 7 8 9 10
            [False, False, False, False, True, False, False, True, False, False, False], # 0 1 2 3 t 5 6 g 8 9 10
            [False, False, True, True, True, True, True, True, False, False, False], # 0 1 ginger 8 9 10
            [False, False, False, False, True, False, False, True, False, False, False], # 0 1 2 3 e 5 6 e 8 9 10
            [False, False, False, False, True, False, False, True, False, False, False], # 0 1 2 3 r 5 6 e 8 9 10
            [False, False, False, False, True, False, True, True, True, False, False], # 0 1 2 3 s 5 dnb 9 10
            [False, False, False, False, False, False, False, True, False, False, False], # 0 1 2 3 4 5 6 h 8 9 10
            [False, False, False, False, False, False, False, True, False, False, False], # 0 1 2 3 4 5 6 o 8 9 10
            [False, False, False, False, True, True, True, True, True, False, False], # 0 1 2 3 aclue 9 10
            [False, False, False, False, False, False, False, True, False, False, False], # 0 1 2 3 4 5 6 s 8 9 10
            [False, False, False, False, False, False, False, True, False, False, False], # 0 1 2 3 4 5 6 e 8 9 10
            ],
            'across_clues': [
                (1, "best anagram for value"),
                (2, "what TikTok used to be called in Jonas' younger days"),
                (3, "Jonas likes his ... cold (according to every standard but his own)"),
                (4, "Jonas does not like to be called a ... (as if brunettes have souls)"),
                (5, f"do not break? drinks not bills? dreams n banking."),
                (6, "this is ..."),
            ],
            'down_clues': [
                (1, "1 across wears a ... better than all of his coworkers"),
                (2, "Jonas likes to spend hours inspecting ..."),
                (7, "artificial intelligence *thumbs up*. artificial ... *thumbs down*"),
                (8, "a supreme graduate program. oh, and a global warming effect.")
            ],
            'solutions':  {
                'across': {
                1: "VAULE",
                2: "MUSICALLY",
                3: "TEA",
                4: "GINGER",
                5: "DNB",
                6: "ACLUE",
                },
                'down': {
                1: "VEST",
                2: "MAPS",
                7: "SWEETNERS",
                8: "GREENHOUSE"
            }           
        }
    }

@backend.route('/')
def index():
    # passing positions func to template
    return render_template('index.html', crossword=crossword_data, positions=positions)

def positions(direction, number):
    """
    Return list of (row, col) coordinate tuples that represent
    the grid cells associated with a given clue.
    Based on specific crossword layout and numbering.
    """
    if direction == 'across':
        if number == 1:
            return [(0, i) for i in range(5)] # VAULE, rad 0
        if number == 2:
            return [(2, i) for i in range(2,11)] # MUSICALLY, rad 2 (9 bokstaver, 11 "plasser")
        if number == 3:
            return [(3, i) for i in range(3)] # TEA, rad 3
        if number == 4:
            return [(7, i) for i in range(2,8)] # GINGER, rad 7
        if number == 5:
            return [(10, i) for i in range(6,9)] # DNB, rad 10
        if number == 6:
            return [(13, i) for i in range(4,9)] # ACLUE, rad 13
    
    elif direction == 'down':
        if number == 1:
            return [(i, 0) for i in range(4)] # VEST, kol 0
        if number == 2:
            return [(i, 2) for i in range(2, 6)] # MAPS, kol 2
        if number == 7:
            return [(i, 4) for i in range(2, 11)] # SWEETNERS, kol 4
        if number == 8:
            return [(i, 7) for i in range(6,16)] # GREENHOUSE, kol 7
    return []

@backend.route('/check', methods=['POST'])
def check_solution():
    """Check the user's crossword solution."""
    if request.is_json:
        user_input = request.get_json()
        correct = True
        solutions = crossword_data['solutions']
        
        # Verify each clue
        for direction, clues in solutions.items():
            for num, solution in clues.items():
                # Construct user answer from inputs
                user_answer = ''.join(
                    user_input.get(f'cell-{i}-{j}', '').upper() for i, j in positions(direction, num)
                )
                # Compare user answer with solution
                if user_answer != solution.upper():
                    correct = False
        
        return jsonify({'correct': correct})
    return jsonify({'error': 'Request must be JSON'}), 400

if __name__ == '__main__':
    backend.run(debug=True)