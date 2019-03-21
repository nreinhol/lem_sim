
target_coefs = [-1, -2, -1, -3]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        print(i, i + n)
        yield l[i:i + n]


for chunk in chunks(target_coefs, 2):
    print(chunk)


def decompose(OptimizationProblem, AMOUNT_AGENTS):
        
        return 