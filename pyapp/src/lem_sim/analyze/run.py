import click as c

from lem_sim import analyze


@c.command()
@c.option('--connection', type=c.Choice(['docker', 'ip']), default='docker')
def run(connection):
    chain_analyzer = analyze.ChainAnalyzer(connection)
    eventlist = chain_analyzer.filter_received_order_event(0, 'latest')
    
    for event in eventlist:
        print(event.keys())


if __name__ == '__main__':
    run()
