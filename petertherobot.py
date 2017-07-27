import os
import praw
import random
import time

from praw.exceptions import APIException

IMAGES = [
    'https://i.redd.it/iup4ly2d9xzy.jpg',
    'https://i.redd.it/nh8ypm8byy0z.jpg',
    'https://i.redd.it/wp13qzplut1z.jpg',
    'https://i.redd.it/nxdtz3hhm85z.jpg',
    'https://i.redd.it/zz0zuuaw2v5z.jpg',
    'https://i.redd.it/g6vx2b4dwj7z.jpg',
    'https://i.redd.it/55xmaosu638z.jpg',
    'https://i.redd.it/yy5brthnxd8z.jpg',
    'https://i.redd.it/n4ajx7vger8z.jpg',
    'https://i.redd.it/ligzit4q5e9z.jpg',
    'https://i.redd.it/aqpbiy8o48az.jpg',
    'https://i.redd.it/c9mjb1jl8maz.jpg',
    'https://i.redd.it/tu98o0mrg0bz.jpg',
]


def main():
    reddit = authenticate()
    comments_replied_to = get_saved_comments()
    while True:
        run_bot(reddit, comments_replied_to)


def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit(
        'petertherobot',
        user_agent='mac:petertherobot:v1 (by /u/nocturne9op2)')
    print("Authenticated as {}".format(reddit.user.me()))

    return reddit


def get_saved_comments():
    if not os.path.isfile('comments_replied_to.txt'):
        comments_replied_to = []
    else:
        with open('comments_replied_to.txt', 'r') as file:
            comments_replied_to = file.read()
            comments_replied_to = comments_replied_to.split("\n")
            del comments_replied_to[-1]

    return comments_replied_to


def run_bot(reddit, comments_replied_to):
    print("Obtaining 25 submissions...")
    for comment in reddit.subreddit('UCI').comments(limit=25):
        trimmed_comment = trim(comment)

        if bool(trimmed_comment) and comment.id not in comments_replied_to \
                and comment.author != reddit.user.me():
            print("String with {} found in comment".format(trimmed_comment))

            try:
                comment.reply(">{}\n\n "
                              "[Here is a picture of Peter the Anteater "
                              "to cheer you up!]({})"
                              .format(trimmed_comment, random.choice(IMAGES)))
                print("Replied to comment " + comment.id)
            except APIException:
                print("RATELIMIT: 'you are replying too much'")
                break

            comments_replied_to.append(comment.id)
            with open('comments_replied_to.txt', 'a') as file:
                file.write(comment.id + "\n")

    print("Sleeping for 10 seconds...")
    time.sleep(10)


def trim(comment):
    if ":(" in comment.body:
        return ":("
    elif ":,(" in comment.body:
        return ":,("
    elif ":'(" in comment.body:
        return ":'("
    else:
        return ""


if __name__ == '__main__':
    main()
