from requests import get
from bs4 import BeautifulSoup
from re import compile
from pandas import DataFrame
from gensim.utils import simple_preprocess
import wikipedia


def search_wiki_awards(name):
    try:
        # Search for the Wikipedia page of the person
        page = wikipedia.page(name)
    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
        try:
        # Search for the Wikipedia page of the person
            page = wikipedia.page('/wiki/'+name)
        except:
            return 0
        # Get the content of the page
    content = page.content
        
    try:
        # Find the section on education
        awards_text = content.split("== Awards ==")[1].split("==")[0]

        return len([s for s in awards_text.splitlines() if len(s) > 3])
    except IndexError:
        return 0


if __name__ == '__main__':

    # Set the base URL for the Wikipedia pages
    base_url = 'https://en.wikipedia.org'
    links_url = 'https://en.wikipedia.org/wiki/List_of_computer_scientists'

    # make the request to the server
    request = get(links_url)

    # get the html content
    response = BeautifulSoup(request.content, 'html')

    content = response.find("div", {"class": "mw-parser-output"}).find_all("ul")

    # create dictionary for scientist name: wiki url pairs
    scientists = {}
    for header in content:
        for scientist in header.find_all("li"):
            link = scientist.find("a", attrs={'href': compile("^/wiki/")})
            if link: scientists[link.text] = link.get("href")


    data = []
    for scientist, page_url in scientists.items():

        # helper variables
        education = ''
        awards = 0
        
        # make the request to the server
        request = get(base_url + page_url)

        # get the html content
        response = BeautifulSoup(request.content, 'html.parser')

        # main content
        content = response.find("div", {"class": "mw-parser-output"})

        # table info of scientist
        table = response.find("table", {"class": "infobox biography vcard"})
            
        # get headers and paragraphs
        header = content.find_all("h2")
        par = content.find_all("p")
        
        # if table exists
        if table:
            # for each row of the body table
            for row in table.find_all("tr"):
                # if there is a Awards header
                if row.find("th", {"class": "infobox-label"}, text=compile("Awards")):
                    # get number  of awards
                    awards = len(row.find_all("li"))
        
        # if page does not contain th of awards in info table
        # try to find awards paragraph
        if not awards:        
            awards = search_wiki_awards(scientist)
        
        # list of desired paragraph ids
        ids = [
                "Education", "Education_and_early_life", "Education_and_career", "Early_life_and_education",
                "Early_life", "Life", "Life_and_career", "Life_and_work", "Biography", "Career"
            ]
        
        # for each header and paragraph
        for h, p in zip(header, par):
            # for each possible span id
            for _id in ids:
                # if header contains one span with _id
                if h.find("span", {"id": _id}):
                    education = p.text # get info
                    break
                
        # append final data
        data += [(scientist, awards, " ".join(simple_preprocess(education)))]


    # convert to pandas DataFrame
    df = DataFrame(data, columns=['Name', 'Awards', 'Education'])

    # drop blank rows
    df = df[df['Education']  != '']

    # some extra text preproccessing
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer

    # stop words vocab
    stop_words = set(stopwords.words('english'))

    # define stemmer object
    stemmer = PorterStemmer()

    # apply preproccessing
    df.loc[:, 'Education'] = df['Education'].apply(lambda doc: ' '.join([stemmer.stem(w) for w in doc.split() if w not in stop_words]))

    # save to csv without taking into account the index
    df.to_csv('List_of_computer_scientists.csv', index=False)

