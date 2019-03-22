def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
                yield l[i:i + n]


def decompose(CentralProblem, variables):
        # split and distribute target coefs
        for index, chunk in enumerate(chunks(CentralProblem.target_coefs, variables.amount_agents)):
                print(chunk, variables.agent_pool[index])

        # split and distribute constraint coefs
        for index, chunk in enumerate(chunks(CentralProblem.individual_resources, variables.amount_agents)):
                print(chunk, variables.agent_pool[index])

        # split and distribute constraint bounds
        for index, chunk in enumerate(chunks(CentralProblem.individual_coefs, variables.amount_agents)):
                print(chunk, variables.agent_pool[index])
