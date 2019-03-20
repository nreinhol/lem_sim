AMOUNT_AGENTS = None
AMOUNT_AGENTS_VARIABLES = None

target_coefs = [-1, -2, -1, -3]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


for chunk in chunks(target_coefs, 2):
    print(chunk)
