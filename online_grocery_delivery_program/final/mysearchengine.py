import urllib.request as urllib2
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import shelve
from django.utils.encoding import smart_str
import ssl


# Create a list of words to ignore
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])



# Bu kelimeleri saymayacagiz:
ignorewords = set(['lang','html','the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', 'if'])

class crawler:
    ''' Bu sinif webde arama yapip aramalari veritabanina aktaracaktir.
    
        v1.0 - crawl dolduruldu
        v0.4 - addLinkRef olusturuldu
        v0.3 - isindexed olusturuldu ve addtoindex dolduruldu. 
        v0.2 - gettextonly ve separatewords fonksiyonlari dolduruldu. Boylece html sayfalarinda ilgili yazilar ayiklanabilir.
        v0.1 - init fonksiyonu guncellendi, createindextables ve close fonksiyonlari tanimlandi
    '''
    
    # Initialize the crawler with the name of database tabs
    def __init__(self, dbtables):
        ''' dbtables bir sozluk olmali:
        
            'urllist': 'urllist.db',
            'wordlocation':'wordlocation.db',
            'link':'link.db',
            'linkwords':'linkwords.db'}
        '''
        self.dbtables = dbtables
    
    def is_tables_ready(self):
        print(hasattr(self, 'urllist') and len(self.urllist)>0)
        return hasattr(self, 'urllist') and len(self.urllist)>0


    # Create the database tables
    def createindextables(self):
        # {url:outgoing_link_count}
        self.urllist = shelve.open(self.dbtables['urllist'], writeback=True, flag='c')

        #{word:{url:[loc1, loc2, ..., locN]}}
        self.wordlocation = shelve.open(self.dbtables['wordlocation'], writeback=True, flag='c')

        #{tourl:{fromUrl:None}}
        self.link = shelve.open(self.dbtables['link'], writeback=True, flag='c')

        #{word:[(urlFrom, urlTo), (urlFrom, urlTo), ..., (urlFrom, urlTo)]}
        self.linkwords = shelve.open(self.dbtables['linkwords'], writeback=True, flag='c')
        
    def close(self):
        if hasattr(self, 'urllist'): self.urllist.close()
        if hasattr(self, 'wordlocation'): self.wordlocation.close()
        if hasattr(self, 'link'): self.link.close()
        if hasattr(self, 'linkwords'): self.linkwords.close()


    # Extract the text from an HTML page (no tags)
    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    # Separate the words by any non-whitespace character
    def separatewords(self, text):
        splitter = re.compile('\\W+')
        return [s.lower() for s in splitter.split(text) if s != '']

            
    # Return true if this url is already indexed
    def isindexed(self, url):
        # urllist = {url:outgoing_link_count}
        if not self.urllist.get(smart_str(url, None)):
            return False
        else:
            return True
    
    # Index an individual page
    def addtoindex(self, url, soup):
        if self.isindexed(url):
            print ('skip', url + ' already indexed')
            return False

        print ('Indexing ' + url)
        url = smart_str(url)
        # Get the individual words
        text = self.gettextonly(soup)
        words = self.separatewords(text)
        
        if 'shel' in words or 'silverstein' in words:
            print("Found it: ", url )
        
        # Record each word found on this page
        for i in range(len(words)):
            word = smart_str(words[i])

            if word in ignorewords:
                continue

            self.wordlocation.setdefault(word, {})

            self.wordlocation[word].setdefault(url, [])
            self.wordlocation[word][url].append(i)

        return True
    
    # Add a link between two pages
    def addlinkref(self, urlFrom, urlTo, linkText):
        fromUrl = smart_str(urlFrom)
        toUrl = smart_str(urlTo)

        if fromUrl == toUrl: return False

        # if not self.link.get(toUrl, None):
        #     self.link[toUrl] = {}

        self.link.setdefault(toUrl, {})
        self.link[toUrl][fromUrl] = None

        words=self.separatewords(linkText)

            
        for word in words:
            word = smart_str(word)

            if word in ignorewords: continue

            self.linkwords.setdefault(word, [])

            self.linkwords[word].append((fromUrl, toUrl))

        return True  
    
    # Starting with a list of pages, do a breadth
    # first search to the given depth, indexing pages
    # as we go
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                           'Accept-Encoding': 'none',
                           'Accept-Language': 'en-US,en;q=0.8',
                           'Connection': 'keep-alive'}
                    req = urllib2.Request(page, headers=hdr)
                    c = urllib2.urlopen(req)
                except Exception as e:
                    print ("Could not open {}, {}".format(page, e))
                    continue
                soup = BeautifulSoup(c.read(), 'html.parser')
                added = self.addtoindex(page, soup)

                if not added:
                    continue

                outgoingLinkCount = 0
                links = soup('a')
                for link in links:
                    if 'href' in link.attrs:
                        url = urljoin(page, link['href'])
                        #os.path.join()
                        if url.find("'") != -1:
                            continue
                            # The fragment identifier introduced
                            # by a hash mark (#) is the optional last
                            # part of a URL for a document. It is typically
                            # used to identify a portion of that document.
                        url = url.split('#')[0]  # remove location portion
                        if url[0:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        added = self.addlinkref(page, url, linkText)
                        if added:
                            outgoingLinkCount += 1

                self.urllist[smart_str(page)] = outgoingLinkCount
            pages = newpages


class searcher:
    def __init__(self,dbtables):
        self.dbtables = dbtables
        self.opendb()

    def __del__(self):
        self.close()

    def close(self):
        try:
            if hasattr(self, 'urllist'): self.urllist.close()
            if hasattr(self, 'wordlocation'): self.wordlocation.close()
            if hasattr(self, 'link'): self.link.close()
            if hasattr(self, 'linkwords'): self.linkwords.close()
            if hasattr(self, 'pagerank'): self.pagerank.close()
        except:
            pass

    def getmatchingpages(self,q):
        results = {}
        # Split the words by spaces
        words = [(smart_str(word).lower()) for word in q.split()]
        if words[0] not in self.wordlocation:
                return results, words

        url_set = set(self.wordlocation[words[0]].keys())

        for word in words[1:]:
            if word not in self.wordlocation:
                return results, words
            url_set = url_set.intersection(self.wordlocation[word].keys())

        for url in url_set:
            results[url] = []
            for word in words:
                results[url].append(self.wordlocation[word][url])

        return results, words

    # Bu kisim Lab odevi icin modifiye edildi
    def getscoredlist(self, results, words, secililer):
        totalscores = dict([(url, 0) for url in results])
        weights = []
        for fonksiyon_ismi, katsayi in secililer.items():
            weights.append(
                (katsayi, self.__getattribute__(fonksiyon_ismi)(results)))

        for (weight,scores) in weights:
            for url in totalscores:
                totalscores[url] += weight*scores.get(url, 0)

        return totalscores

    # Bu kisim Lab odevi icin modifiye edildi
    def query(self,q, secililer):

        results, words = self.getmatchingpages(q)
        if len(results) == 0:
            print ('No matching pages found!')
            return

        scores = self.getscoredlist(results,words, secililer)
        rankedscores = sorted([(score,url) for (url,score) in scores.items()],reverse=True)
        return rankedscores[0:10]
            

    def normalizescores(self,scores,smallIsBetter=0):
        vsmall = 0.00001 # Avoid division by zero errors
        if smallIsBetter:
            minscore=min(scores.values())
            minscore=max(minscore, vsmall)
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) \
                         in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0:
                maxscore = vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    def frequencyscore(self, results):
        counts = {}
        for url in results:
            score = 1
            for wordlocations in results[url]:
                score *= len(wordlocations)
            counts[url] = score
        return self.normalizescores(counts, smallIsBetter=False)

    def locationscore(self, results):
        locations=dict([(url, 1000000) for url in results])
        for url in results:
            score = 0
            for wordlocations in results[url]:
                score += min(wordlocations)
            locations[url] = score
        return self.normalizescores(locations, smallIsBetter=True)

    def worddistancescore(self, result):
        urller = result.keys()
        listoflist = result.values()
        counts = {}
        mesafe = 1000000
        if (len(listoflist)) < 2 or (len(urller)) < 2:
            for url in result:
                counts[url] = 1.0
            return counts

        for url in urller:
            for i in range(len(result[url])-1):
                for j in range(len(result[url][i])):
                    for k in range(len(result[url][i+1])):
                        if mesafe > abs(result[url][i][j]-result[url][i+1][k]):
                            mesafe = abs(result[url][i][j]-result[url][i+1][k])

            counts[url]=mesafe

        return self.normalizescores(counts, smallIsBetter=1)
        
    def inboundlinkscore(self, results):
        inboundcount=dict([(url, len(self.link[url])) for url in results if url in self.link])
        return self.normalizescores(inboundcount)

    def pagerankscore(self, results):
        self.pageranks = dict([(url, self.pagerank[url]) for url in results if url in self.pagerank])

        return self.normalizescores(self.pageranks, smallIsBetter=False)

    def calculatepagerank(self,iterations=20):
        # clear out the current page rank table
        # {url:pagerank_score}

        # initialize every url with a page rank of 1
        for url in self.urllist:
            #print (url)
            self.pagerank[url] = 1.0

        for i in range(iterations):
            print ("Iteration {}".format(i))
            for url in self.urllist:
                #print (url , self.pagerank[url])
                #print (self.link[url])
                pr=0.15
                # Loop through all the pages that link to this one
                for linker in self.link[smart_str(url)]:
                    linkingpr = self.pagerank[smart_str(linker)]
                    #print (linker, linkingpr)


                    # Get the total number of links from the linker
                    linkingcount = self.urllist[linker]
                    #print (linkingcount)
                    pr += 0.85*(linkingpr/linkingcount)

                self.pagerank[url] = pr

    # Open the database tables
    def opendb(self):
        # {url:outgoing_link_count}
        self.urllist = shelve.open(self.dbtables['urllist'], writeback=True, flag='r')
        #{word:{url:[loc1, loc2, ..., locN]}}
        self.wordlocation = shelve.open(self.dbtables['wordlocation'], writeback=True, flag='r')
        #{tourl:{fromUrl:None}}
        self.link = shelve.open(self.dbtables['link'], writeback=True, flag='r')
        #{word:[(urlFrom, urlTo), (urlFrom, urlTo), ..., (urlFrom, urlTo)]}
        self.linkwords = shelve.open(self.dbtables['linkwords'], writeback=True, flag='r')
        # {url:pagerank_score}
        self.pagerank = shelve.open(self.dbtables['pagerank'], writeback=True, flag='c')

    # Bu kisim Lab odevi icin sonradan eklendi
    def is_pagerank_populated(self):
        ''' PageRank DB si olusturuldu mu kontrol ediyoruz.

            TODO: En son yapilan pagerank hesaplama kodunun zamani da DB de tutularak, 
            kullanici tarafindan secilen bir zaman araligi kadar eski olmasi durumunda false dondurulebilir
        '''
        return len(self.pagerank)>0

    def get_linkwords_from_url(self, url):
        for word, url_tuple_listesi in self.linkwords.items():
            for url_tuples in url_tuple_listesi:
                if url == url_tuples[1]:
                    # linkwords icindeki ikinci eleman, o linke basilarak gidilen sayfayi belirtir.
                    print(url, url_tuples, word)
                    return word
        return 'AnaSayfa' # Eger herhangi bir url gelmediyse, kelime ana sayfada bulunmustur

