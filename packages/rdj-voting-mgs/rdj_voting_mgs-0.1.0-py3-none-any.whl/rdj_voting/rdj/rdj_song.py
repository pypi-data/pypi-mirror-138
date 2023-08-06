import requests

from rdj_voting.ressources import RDJ_VOTING, get_logger

_logger = get_logger(__name__)


class RdjSong:

    def __init__(self, song_title, artist_name, song_list, song_id):
        self.song_title = song_title
        self.artist_name = artist_name
        self.song_id = song_id
        self.song_list = song_list

    def send_voting(self, verbose=False):
        voting_url = RDJ_VOTING.format(self.song_list, self.song_id)
        result = requests.get(voting_url)
        if verbose:
            _logger.info("{}, {} for : {} - {}".format(result.status_code, result.text, self.song_title, self.artist_name))
        return result.status_code == 200
