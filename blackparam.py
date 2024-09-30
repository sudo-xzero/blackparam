import requests
import argparse
from colorama import init, Fore, Style
from bs4 import BeautifulSoup
from urllib.parse import urljoin

init(autoreset=True)

print(Fore.RED + """
██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗  █████╗ ██████╗  █████╗ ███╗   ███╗
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗████╗ ████║
██████╔╝██║     ███████║██║     █████╔╝ ██████╔╝███████║██████╔╝███████║██╔████╔██║
██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██╔═══╝ ██╔══██║██╔══██╗██╔══██║██║╚██╔╝██║
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗██║     ██║  ██║██║  ██║██║  ██║██║ ╚═╝ ██║
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
""" + Style.RESET_ALL)

parser = argparse.ArgumentParser(description="This tool is used to extract URLs from the web archive.")
parser.add_argument("-d", "--domain", help="The target domain", required=True)
args = parser.parse_args()

target_domain = args.domain
print("-------------------------------------------------------------")
print(Style.BRIGHT + Fore.GREEN + "Now extracting the URLs, please wait... " + Style.RESET_ALL)
print("-------------------------------------------------------------")

api_url = f"https://web.archive.org/cdx/search/cdx?url=*.{target_domain}/*&output=json&collapse=urlkey"
response = requests.get(api_url)
response.raise_for_status()

data = response.json()
urls = [entry[2] for entry in data[1:] if len(entry) > 2]

class SimpleCrawler:
    def __init__(self, start_url):
        self.visited = set()
        self.to_visit = [start_url]

    def extract_links_and_files(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            links = {urljoin(url, a['href']) for a in soup.find_all('a', href=True)}
            files = {urljoin(url, script['src']) for script in soup.find_all('script', src=True)}

            return links, files
        except Exception as e:
            print(f"Failed to extract links from {url}: {e}")
            return set(), set()

    def crawl(self):
        all_files = set()
        while self.to_visit:
            url = self.to_visit.pop(0)
            if url in self.visited:
                continue
            self.visited.add(url)
            links, files = self.extract_links_and_files(url)
            all_files.update(files)
            self.to_visit.extend(links - self.visited)
        return all_files

if __name__ == "__main__":
    print("Extracted URLs from the archive:")
    for url in urls:
        print(url)
        crawler = SimpleCrawler(url)
        files = crawler.crawl()
        if files:
            print("Extracted files:")
            for file in files:
                print(file)
