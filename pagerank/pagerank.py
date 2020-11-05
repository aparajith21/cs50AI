import os
import random
import re
import sys
from copy import deepcopy
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    dist = {} #create a dictionary
    link_number = len(corpus[page]) #number of links from the current page)
    page_number = len(corpus) #number of pages
    if link_number:
        for Page in corpus:
            dist[Page] = (1 - damping_factor)/ page_number #add random choosing

        for link in corpus[page]:
            dist[link] += damping_factor / link_number #account for pages current page links to
    else:
        for page in corpus: #if it links to nothing, then it's a random selection with equal probability for entering each page
            dist[page] = 1 / page_number

    return dist
    
        


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {}#create a dictionary
    page = random.choice(list(corpus.keys())) #pick a page pseudorandomly
    for page in corpus:
        rank[page] = 0 #initialise the dictionary

    for i in range(n):
        dist = transition_model(corpus, page,damping_factor) #transition model of current page
        for page in rank:
            rank[page] = (i * rank[page] + dist[page])/(i + 1) #rank calculation based on number of iterations completed.
        page = random.choices(list(rank.keys()), list(rank.values()))[0] #random generation of a page weighted based on the rank obtained till the next iteration

    return rank

    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_number = len(corpus) #number of pages
    
    rank = {} # create a dictionary
    
    for page in corpus:
        rank[page] = 1 / page_number #initialise
       
    dist = deepcopy(rank) #copy rank to check difference
    different = True #continue iterating as long as difference is > 0.001
    while different:
        different = False #assume there's no difference initially
        for page in corpus:
            pr = 0 #initial sum of page ranks of all pages linking to current page
            for linker_page in corpus:
                if page in corpus[linker_page]:
                    pr += rank[linker_page] / len(corpus[linker_page]) #pagerank sum
                if not len(corpus[linker_page]):
                    pr += rank[linker_page] / page_number #incase no links
            
            dist[page] = (1 - damping_factor) / page_number + damping_factor * pr #new pagerank of current page
        for page in corpus:
            if abs(rank[page] - dist[page]) > 0.001: #if even a single page is different, reiterate
                different = True
            rank[page] = dist[page] #copy to rank
        
    return rank


if __name__ == "__main__":
    main()
