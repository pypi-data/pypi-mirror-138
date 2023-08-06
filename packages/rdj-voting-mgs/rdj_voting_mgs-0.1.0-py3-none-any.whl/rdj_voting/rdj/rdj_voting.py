import requests
import re
from html.parser import HTMLParser

from bs4 import BeautifulSoup
from rdj_voting.ressources import RDJ_URL
from rdj_voting.rdj.rdj_song import RdjSong


class RdjVoting:

    def __init__(self, url=RDJ_URL):
        self.url = url

    def get_song_list(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        block_song = soup.select('#dago tr')
        all_song = []
        for block in block_song:
            content_detail = block.contents[5].text.split('\n')
            link_click = BeautifulSoup(str(block.contents[7]), 'html.parser').select('a')[0].attrs['onclick']
            extract_list_id = re.findall(r'\d+',link_click)
            song = RdjSong(content_detail[0], content_detail[1], extract_list_id[0], extract_list_id[1])
            all_song.append(song)
        return all_song
