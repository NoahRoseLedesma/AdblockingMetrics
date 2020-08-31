from OpenWPM.automation import CommandSequence, TaskManager
import argparse

NUM_BROWSERS = 2

sites = []
with open("sources.csv") as file:
    for line in file:
        sites.append("http://" + line.replace("\n", "").split(',')[1])
        if len(sites) == 100:
            break

manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    browser_params[i]['http_instrument'] = True
    # Record cookie changes
    browser_params[i]['cookie_instrument'] = True
    # Record JS Web API calls
    browser_params[i]['js_instrument'] = True
    # Enable/Disable ad blocking
    browser_params[i]["ublock-origin"] = False
    # Use headless/headful mode
    browser_params[i]['display_mode'] = 'headless'

    # Do not record Navigations
    browser_params[i]['navigation_instrument'] = False
    # Do not record the callstack of all WebRequests made
    browser_params[i]['callstack_instrument'] = False


# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = './output/vanilla/'
manager_params['log_directory'] = './output/vanilla/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites
for site in sites:

    # Parallelize sites over all number of browsers set above.
    command_sequence = CommandSequence.CommandSequence(
        site, reset=True,
        callback=lambda success, val=site:
        print("CommandSequence {} done".format(val)))

    # Start by visiting the page
    command_sequence.get(sleep=3, timeout=60)

    # Run commands across the three browsers (simple parallelization)
    manager.execute_command_sequence(command_sequence)

# Shuts down the browsers and waits for the data to finish logging
manager.close()