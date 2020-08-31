# Methods and constants used across multiple data analysis scripts
import os
from typing import Tuple, Dict, Set, List
import tldextract
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import rcParams

VANILLA_DATASET_PATH = "./output/vanilla/crawl-data.sqlite"
AD_BLOCKING_DATASET_PATH = "./output/ad_blocking/crawl-data.sqlite"
FIGURES_DIR_PATH = "./output/figures/"

def GetDatabases() -> Tuple[object, object]:
    return (sqlite3.connect(VANILLA_DATASET_PATH), sqlite3.connect(AD_BLOCKING_DATASET_PATH))

def GetVisitedDomains(database: object) -> Set[str]:
    domains = set()
    for row in database.execute("SELECT site_url FROM site_visits"):
        domains.add(tldextract.extract(row[0]).registered_domain)
    return domains

# Return a dict mapping visit ids to the top level domain
def GetVisitedDomainsDict(database: object) -> Dict[int, str]:
    domains = dict()
    for row in database.execute("SELECT visit_id, site_url FROM site_visits"):
        domains[row[0]] = tldextract.extract(row[1]).registered_domain
    return domains


def PrintTopResults(data: Dict, counted_object_name: str) -> None:
    sorted_results = sorted(data.items(), key=lambda x: x[1], reverse=True)
    for i in range(10):
        print("#{}: {} with {} {}".format(str(i+1), sorted_results[i][0], sorted_results[i][1], counted_object_name))


def GetPathForFigure(figname: str) -> str:
    return os.path.join(FIGURES_DIR_PATH, figname)

def MakePlots(vanilla_values: List, ad_blocking_values: List, counted_object_name: str) -> None:
    rcParams.update({'figure.autolayout': True})

    sns.catplot(data=pd.DataFrame({"Vanilla" : vanilla_values, "Ad-blocking" : ad_blocking_values}), kind="point")
    plt.ylabel("# of third-party {} per site".format(counted_object_name))
    plt.xlabel("Instrumentation")
    plt.savefig(GetPathForFigure("{}_per_visited_site.png".format(counted_object_name.lower().replace(' ', '_'))))

    plt.clf()

    sns.distplot(vanilla_values, hist=False, label="Vanilla browser")
    sns.distplot(ad_blocking_values, hist=False, label="Ad-blocking browser")
    plt.ylabel("Kernel Density Estimate")
    plt.xlabel("# of third-party HTTP requests per site")
    plt.xlim(left=0)
    plt.savefig(GetPathForFigure("kde_{}.png".format(counted_object_name.lower().replace(' ', '_'))))