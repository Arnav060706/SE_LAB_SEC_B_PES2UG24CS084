
def feedback(code, guess):
    exact = 0
    partial = 0

    code_used = [False] * len(code)
    guess_used = [False] * len(guess)

    # First pass: count exact matches.
    for i in range(min(len(code), len(guess))):
        if code[i] == guess[i]:
            exact += 1
            code_used[i] = True
            guess_used[i] = True

    # Second pass: count partial matches.
    for i in range(len(guess)):
        if guess_used[i]:
            continue

        for j in range(len(code)):
            if not code_used[j] and guess[i] == code[j]:
                partial += 1
                code_used[j] = True
                guess_used[i] = True
                break

    return exact, partial