import logging
from datetime import datetime

from lem_sim import PROJECT_DIR

start_time_string = datetime.now().strftime('%d.%m.%Y_%H:%M')
logging.basicConfig(format='', filename='{}/logs/{}_simulation.log'.format(PROJECT_DIR, start_time_string),
                    level=logging.INFO)


def log_initial_setup(var):
    logging.info('__________________________________ ')
    logging.info('CENTRAL LP')
    logging.info(var.central_problem)
    logging.info('__________________________________ ')
    logging.info('INITIAL SETUP')
    logging.info(var.dealer)

    for agent in var.agent_pool:
        logging.info('\n{}'.format(agent))


def log_iteration_stats(var, iteration):
    logging.info('\n__________________________________')
    logging.info('ITERATION {}'.format(iteration))
    logging.info(var.dealer)

    for agent in var.agent_pool:
        logging.info('\n{}'.format(agent))


def log_verify_strong_duality_failed(agent):
        logging.info('\n{} did not accept the trades bill!'.format(agent.name))
