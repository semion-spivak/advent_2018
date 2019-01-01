
def get_score(x, y):
    combined = x + y
    if combined > 9:
        return (1, combined % 10)
    else:
        return (combined,)


def main():
    scores_num = 293801
    scores = [3, 7]
    a_idx, b_idx = 0, 1

    def tick():
        nonlocal scores, a_idx, b_idx
        score_a = scores[a_idx]
        score_b = scores[b_idx]
        scores.extend(get_score(score_a, score_b))
        a_idx = (a_idx + score_a + 1) % len(scores)
        b_idx = (b_idx + score_b + 1) % len(scores)

    while len(scores) < scores_num + 10:
        tick()

    print(f'part 1 :{"".join(map(str, scores[scores_num:scores_num+10]))}')

    scores = [3, 7]
    a_idx, b_idx = 0, 1
    found = False
    window_idx = 0
    i = 0
    template = list(map(int, str(scores_num)))
    template_len = len(template)

    while not found:
        tick()

        if len(scores) < template_len:
            continue

        for i in range(window_idx, len(scores) - template_len):
            if template == scores[i:i+template_len]:
                found = True
                break
        else:
            window_idx = i+1

    print(f'part 2: {window_idx+1}')


if __name__ == '__main__':
    main()
