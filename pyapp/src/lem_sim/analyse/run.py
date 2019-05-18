import click as c

from lem_sim import analyse


@c.command()
@c.option('--analyse', type=c.Choice(['events']))
def run(analyse):
    event_handler = analyse.EventHandler()
    eventlist = event_handler.filter_received_order_event(0, 'latest')
    
    for event in eventlist:
        print(event['args'], event['blockNumber'])


if __name__ == '__main__':
    run()