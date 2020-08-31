from common import *

import tldextract
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

vanilla, ad_blocking = GetDatabases()
visited_domains = GetVisitedDomains(vanilla)

def analyze_calls_for_dataset(dataset):
    # Maps a third party domain to the number of JS API calls it makes across all pages crawled 
    num_calls_by_third_party = dict()
    # Maps a domain to the number of JS API calls made by third party scripts on the visited page
    num_third_party_calls_by_domain = dict()

    for visited_domain in visited_domains:
        num_third_party_calls_by_domain[visited_domain] = 0
        result = dataset.execute("SELECT script_url FROM javascript WHERE top_level_url LIKE '%{}%'".format(visited_domain))
        for row in result:
            script_domain = tldextract.extract(row[0]).registered_domain
            if script_domain != visited_domain:
                if script_domain not in num_calls_by_third_party:
                    num_calls_by_third_party[script_domain] = 0
                num_calls_by_third_party[script_domain] += 1
                num_third_party_calls_by_domain[visited_domain] += 1 

    return (num_calls_by_third_party, num_third_party_calls_by_domain)

vanilla_results = analyze_calls_for_dataset(vanilla)
ad_blocking_results = analyze_calls_for_dataset(ad_blocking)

# Print some results
print("Domains with the most third party JS calls in vanilla:")
PrintTopResults(vanilla_results[1], "calls")
print("\nDomains with the most third party JS calls in ad-blocking:")
PrintTopResults(ad_blocking_results[1], "calls")
print("\nTop third-party sites to make JS calls in vanilla:")
PrintTopResults(vanilla_results[0], "calls")
print("\nTop third-party sites to make JS calls in ad-blocking:")
PrintTopResults(ad_blocking_results[0], "calls")

# Plot the results
MakePlots(list(vanilla_results[1].values()), list(ad_blocking_results[1].values()), "JS Calls")