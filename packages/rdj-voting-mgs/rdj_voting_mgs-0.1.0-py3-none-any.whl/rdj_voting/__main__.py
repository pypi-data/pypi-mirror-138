import argparse
import random
import time

from rdj_voting.rdj.rdj_voting import RdjVoting
from rdj_voting.ressources import get_logger

parser = argparse.ArgumentParser(description="""
    RJD Automatic Voting,
    If you don't add any arguments, the script will vote one time for all the songs available on the site
""")
group = parser.add_argument_group()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-n", "--number", help="number of votes to cast", type=int)
parser.add_argument("-l", "--list", help="song list, recoverable on the voting link on the site", type=int)
group.add_argument("-r", "--random", help="make random votes", action="store_true")
group.add_argument("-c", "--choice", help="number of songs to vote randomly", type=int, default=1)
parser.add_argument("-i", "--idSong",
                    help="choose the id of the song to vote, if specified, the other filters are not taken into account",
                    type=int)
args = parser.parse_args()

verbosity = args.verbose

_logger = get_logger(__name__)


def vote_all_song(all_song):
    """
    Vote all_song
    :param all_song: list of song
    :return: None
    """
    for song in all_song:
        wait_random = int(random.random() * 10)
        song.send_voting(verbosity)
        time.sleep(wait_random)


def main():
    vote = RdjVoting()
    all_song = vote.get_song_list()
    if args.idSong:
        all_song = list(filter(lambda item: item.song_id == str(args.idSong), all_song))
    if args.list and not args.idSong:
        all_song = list(filter(lambda item: item.song_list == str(args.list), all_song))
    if args.random and not args.idSong:
        all_song = random.choices(all_song, k=args.choice)
    if args.number:
        for _ in range(args.number):
            vote_all_song(all_song)
    else:
        vote_all_song(all_song)


if __name__ == '__main__':
    main()
