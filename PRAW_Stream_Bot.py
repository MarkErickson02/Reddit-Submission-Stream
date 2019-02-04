import praw
import config
import time
from praw.exceptions import PRAWException
from prawcore.exceptions import PrawcoreException
from matplotlib import pyplot as plt


class StreamBot:

    posts = {}
    reddit = None

    def authenticate(self):
        reddit = praw.Reddit(client_id=config.client_id,
                             client_secret=config.client_secret,
                             user_agent=config.user_agent,
                             username=config.username,
                             password=config.password
                             )
        self.reddit = reddit

    def monitor_subreddit(self):
        start_timer = time.clock()
        subreddit = self.reddit.subreddit('all')
        for submissions in subreddit.stream.submissions():
            try:
                if submissions.author is None:
                    print(submissions.title)
                if submissions.subreddit is None:
                    print("Subreddit not found")
                else:
                    print(submissions.author, " submitted ", submissions.title, " to ", submissions.subreddit)
                    self.check_user_stats(submissions.author)
                    self.add_posts_to_dictionary(submissions.subreddit, start_timer)
            except PRAWException as err:
                print("Error detected: ", err)
            except KeyboardInterrupt:
                break
        self.choose_next_action()

    def choose_next_action(self):
        user_action = input("Press g to graph, s to stream more data or p to print the entire dictionary")
        user_action.lower()
        if user_action == 'g':
            self.graph_total_posts()
        if user_action == 's':
            self.monitor_subreddit()
        else:
            print("Value not recognized")

    def add_posts_to_dictionary(self, subreddit, start_timer):
        if not (self.posts.get(subreddit)):
            self.posts[subreddit] = 1
        else:
            self.posts[subreddit] += 1
        end_timer = time.clock()
        self.sort_and_print_dict(self.posts)
        print(end_timer - start_timer)

    def check_user_stats(self, user):
        user_posts = {}
        try:
            for submission in user.submissions.top('all'):
                if not (user_posts.get(submission.subreddit)):
                    user_posts[submission.subreddit] = 1
                else:
                    user_posts[submission.subreddit] += 1
            self.sort_and_print_dict(user_posts)
        except PRAWException as err:
            print(err)
        except PrawcoreException as err:
            print(err)

    @staticmethod
    def sort_and_print_dict(user_posts):
        sorted_dict_values = reversed(sorted(user_posts.items(), key=lambda kv: kv[1]))
        count = 0
        for sub_name, posts in sorted_dict_values:
            if count < 1:
                print("Sub: {}, # of Posts: {}".format(sub_name, posts))
            count += 1

    def graph_total_posts(self):
        plt.bar(str(self.posts.values), str(self.posts.keys))
        plt.xlabel("Subreddits")
        plt.ylabel("Posts")
        for sub_name, posts in self.posts.items():
            plt.plot(sub_name.display_name, posts)
        plt.show()


def main():
    bot = StreamBot()
    bot.authenticate()
    bot.monitor_subreddit()


if __name__ == "__main__":
    main()
