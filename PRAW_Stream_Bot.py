from praw.exceptions import PRAWException
import DictionaryUtility
import UserStatistics
import config
import praw
import time


class StreamBot:

    _posts = {}
    _reddit = None
    _user_stats = None
    _utility = None

    def __init__(self):
        self._utility = DictionaryUtility.DictionaryUtility()
        self._user_stats = UserStatistics.UserStatistics()
        self.authenticate()

    def authenticate(self):
        reddit = praw.Reddit(client_id=config.client_id,
                             client_secret=config.client_secret,
                             user_agent=config.user_agent,
                             username=config.username,
                             password=config.password
                             )
        self._reddit = reddit

    def check_background_of_posters(self, submission_id):

        start_timer = time.clock()
        user_submission_frequency = []
        submission = self._reddit.submission(submission_id)
        user_submission_frequency.append(self._user_stats.check_user_submissions(submission.author))
        end_timer = time.clock()
        submission.comments.replace_more(limit=0)
        print("Fetch and replace comments time: ", end_timer - start_timer)
        comments = submission.comments.list()
        for comment in comments:
            user_submission_frequency.append(self._user_stats.check_user_submissions(comment.author))
        end_timer = time.clock()
        print("put comments in dictionary time: ", end_timer - start_timer)
        combined_submission_dict = {}
        for user_dict in user_submission_frequency:
            combined_submission_dict.update(user_dict)
        end_timer = time.clock()
        print("Combining dictionaries time: ", end_timer - start_timer)
        self._utility.sort_and_print_dict(combined_submission_dict, limit=len(combined_submission_dict))
        self._utility.bar_graph_total_submission(combined_submission_dict)

    def monitor_subreddit(self, included_nsfw=True, show_stream=True):
        start_timer = time.clock()
        subreddit = self._reddit.subreddit('all')
        for submissions in subreddit.stream.submissions():
            try:
                if submissions.author is None:
                    print(submissions.title)
                if submissions.subreddit is None:
                    print("Subreddit not found")
                else:
                    if included_nsfw is False and submissions.over_18:
                        print("censored")
                        continue
                    if show_stream is True:
                        print(submissions.author, " submitted ", submissions.title, " to ", submissions.subreddit)
                        self._user_stats.check_user_submissions(submissions.author)
                        self.add_posts_to_dictionary(submissions.subreddit, start_timer)
            except PRAWException as err:
                print("Error detected: ", err)

    def choose_next_action(self):
        user_action = input("Press g to graph, s to stream more data, p to print data, b to stream in background: ")
        user_action.lower()
        if user_action == 'g':
            self._utility.bar_graph_total_submission(self._posts)
        if user_action == 's':
            self.monitor_subreddit()
        if user_action == 'p':
            self._utility.sort_and_print_dict(len(self._posts))
        if user_action == 'b':
            self.monitor_subreddit(show_stream=False)
        else:
            print("Value not recognized")

    def add_posts_to_dictionary(self, subreddit, start_timer):
        if not (self._posts.get(subreddit)):
            self._posts[subreddit] = 1
        else:
            self._posts[subreddit] += 1
        end_timer = time.clock()
        self._utility.sort_and_print_dict(self._posts)
        print(end_timer - start_timer)


def main():
    bot = StreamBot()
    sub_id = input("Enter id of submission: ")
    bot.check_background_of_posters(sub_id)
    # bot.choose_next_action()


if __name__ == "__main__":
    main()
