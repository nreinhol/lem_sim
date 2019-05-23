import click as c

from lem_sim import analyse


@c.command()
@c.option('--option', type=c.Choice(['events']))
def run(option):

    if(option == 'events'):
        event_handler = analyse.EventHandler()
        received_order_events = event_handler.filter_received_order_event(0, 'latest')
        stored_trade_events = event_handler.filter_stored_trade_event(0, 'latest')
        fetched_trade_events = event_handler.filter_fetched_trade_event(0, 'latest')
        rejected_trade_events = event_handler.filter_rejected_trade_event(0, 'latest')

        print('\nRECEIVED ORDERS')
        for event in received_order_events:
                print(event['args'], event['blockNumber'])

        print('\nSTORED TRADES')
        for event in stored_trade_events:
                print(event['args'], event['blockNumber'])

        print('\nFETCHED TRADES')
        for event in fetched_trade_events:
                print(event['args'], event['blockNumber'])

        print('\nREJECTED TRADES')
        for event in rejected_trade_events:
                print(event['args'], event['blockNumber'])


if __name__ == '__main__':
    run()
