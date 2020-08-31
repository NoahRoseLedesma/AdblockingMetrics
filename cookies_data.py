from common import *

import tldextract
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

vanilla, ad_blocking = GetDatabases()
visited_domains = GetVisitedDomainsDict(vanilla)

def analyze_cookies_for_dataset(dataset):
    # Maps a third party domain to the number of cookies it stores across all pages crawled
    num_cookies_by_third_party = dict()
    # Maps a top level domain to the number of third party cookies stored
    num_third_party_cookies_by_domain = dict()

    for visit_id, visited_domain in visited_domains.items():
        if not visited_domain in num_third_party_cookies_by_domain:
            num_third_party_cookies_by_domain[visited_domain] = 0
        result = dataset.execute("SELECT host FROM javascript_cookies WHERE visit_id={} AND host NOT LIKE '%{}' GROUP BY name".format(visit_id, visited_domain))
        for row in result:
            cookie_host_domain = tldextract.extract(row[0]).registered_domain
            if cookie_host_domain not in num_cookies_by_third_party:
                num_cookies_by_third_party[cookie_host_domain] = 0
            num_cookies_by_third_party[cookie_host_domain] += 1
            num_third_party_cookies_by_domain[visited_domain] += 1 

    return (num_cookies_by_third_party, num_third_party_cookies_by_domain)

vanilla_results = analyze_cookies_for_dataset(vanilla)
ad_blocking_results = analyze_cookies_for_dataset(ad_blocking)

# Print some results
print("Domains with the most third party cookies in vanilla:")
PrintTopResults(vanilla_results[1], "cookies")
print("\nDomains with the most third party cookies in ad-blocking:")
PrintTopResults(ad_blocking_results[1], "cookies")
print("\nTop third-party sites to store cookies in vanilla:")
PrintTopResults(vanilla_results[0], "cookies")
print("\nTop third-party sites to store cookies in ad-blocking:")
PrintTopResults(ad_blocking_results[0], "cookies")

# Plot the results
MakePlots(list(vanilla_results[1].values()), list(ad_blocking_results[1].values()), "Cookies")