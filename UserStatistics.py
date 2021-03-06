from prawcore.exceptions import PrawcoreException
from praw.exceptions import PRAWException


class UserStatistics:

    def check_user_submissions(self, user):
        user_posts = {}
        try:
            for submission in user.submissions.top('all'):
                if not (user_posts.get(submission.subreddit)):
                    user_posts[submission.subreddit] = 1
                else:
                    user_posts[submission.subreddit] += 1
        except PRAWException as err:
            print(err)
        except PrawcoreException as err:
            print(err)
        return user_posts

    def check_user_comments(self, user):
        user_submissions = {}
        try:
            for comment in user.comments.top('all'):
                if not (user_submissions.get(comment.subreddit)):
                    user_submissions[comment.subreddit] = 1
                else:
                    user_submissions[comment.subreddit] += 1
        except PrawcoreException as err:
            print(err)
        return user_submissions

    def find_users_words(self, user):
        user_words = {}
        try:
            for submission in user.submissions.top('all'):
                for word in submission.title.split():
                    if not (user_words.get(word)):
                        user_words[word] = 1
                    else:
                        user_words[word] += 1
            for comment in user.comments.top('all'):
                for word in comment.body.split():
                    if not (user_words.get(word)):
                        user_words[word] = 1
                    else:
                        user_words[word] += 1
        except PRAWException as err:
            print(err)
        except PrawcoreException as err:
            print(err)
        return user_words