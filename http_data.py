from common import *

import tldextract
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os

vanilla, ad_blocking = GetDatabases()
visited_domains = GetVisitedDomains(vanilla)

def analyze_http_requests_for_dataset(dataset):
    num_requests_by_third_party_domain = dict()
    num_third_party_requests_by_visited_site = dict()

    for visited_domain in visited_domains:
        result = dataset.execute("SELECT url FROM http_requests WHERE top_level_url LIKE '%{}%'".format(visited_domain))
        num_third_party_requests_by_visited_site[visited_domain] = 0
        for row in result:
            requested_domain = tldextract.extract(row[0]).registered_domain
            if visited_domain != requested_domain:
                if not requested_domain in num_requests_by_third_party_domain:
                    num_requests_by_third_party_domain[requested_domain] = 0
                num_requests_by_third_party_domain[requested_domain] += 1
                num_third_party_requests_by_visited_site[visited_domain] += 1
    return (num_requests_by_third_party_domain, num_third_party_requests_by_visited_site)

vanilla_results = analyze_http_requests_for_dataset(vanilla)
ad_blocking_results = analyze_http_requests_for_dataset(ad_blocking)

# Print some results
print("Domains with the most third party requests in vanilla:")
PrintTopResults(vanilla_results[1], "requests")
print("\nDomains with the most third party requests in ad-blocking:")
PrintTopResults(ad_blocking_results[1], "requests")
print("\nTop third-party sites to receive requests in vanilla:")
PrintTopResults(vanilla_results[0], "requests")
print("\nTop third-party sites to receive requests in ad-blocking:")
PrintTopResults(ad_blocking_results[0], "requests")


# Plot the results
MakePlots(list(vanilla_results[1].values()), list(ad_blocking_results[1].values()), "HTTP Requests")