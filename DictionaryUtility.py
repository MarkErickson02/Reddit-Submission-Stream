from matplotlib import pyplot as plt


class DictionaryUtility:

    @staticmethod
    def sort_and_print_dict(user_posts, limit=1):
        sorted_dict_values = reversed(sorted(user_posts.items(), key=lambda kv: kv[1]))
        count = 0
        for sub_name, posts in sorted_dict_values:
            if count < limit:
                print("Sub: {}, # of Posts: {}".format(sub_name, posts))
            count += 1

    @staticmethod
    def bar_graph_total_submission(dict_of_submissions):
        plt.bar(range(len(dict_of_submissions)), list(dict_of_submissions.values()), align="center")
        plt.xlabel("Subreddits")
        plt.ylabel("Number of Posts")
        plt.xticks(range(len(dict_of_submissions)), list(dict_of_submissions.keys()))
        plt.show()
