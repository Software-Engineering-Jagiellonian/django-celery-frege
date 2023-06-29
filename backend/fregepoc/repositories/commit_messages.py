import re
import string
import textstat
from typing import List
from nltk.tokenize import TweetTokenizer

from fregepoc.repositories.constants import CommitMessagesTypes
from fregepoc.repositories.models import CommitMessage


class CommitMessagesQualityRepoAnalyzer:

    def __init__(self, commit_messages: List[CommitMessage]):
        self.commit_messages = commit_messages
        self.commits_amount = len(commit_messages)
        self.average_commit_message_length = self._calculate_average_commit_message_length()
        self.average_commit_message_words_amount = self._calculate_average_commit_message_words_amount()
        self.percentage_of_unclassified_commits = self._calculate_percentage_of_unclassified_commits()
        self.percentage_of_merge_pr_commits = self._calculate_percentage_of_merge_pr_commits()
        self.percentage_of_config_change_commits = self._calculate_percentage_of_config_change_commits()
        self.percentage_of_fix_commits = self._calculate_percentage_of_fix_commits()
        self.percentage_of_feature_commits = self._calculate_percentage_of_feature_commits()
        self.classified_to_unclassified_cm_ratio = self._calculate_classified_to_unclassified_cm_ratio()
        self.average_commit_message_fog_index = self._calculate_average_commit_message_fog_index()

    def _calculate_average_commit_message_length(self):
        if self.commits_amount == 0:
            return 0
        else:
            return sum(commit_message.commit_message_char_length for commit_message in
                       self.commit_messages) / self.commits_amount

    def _calculate_average_commit_message_words_amount(self):
        if self.commits_amount == 0:
            return 0
        else:
            return sum(commit_message.words_amount for commit_message in self.commit_messages) / self.commits_amount

    def _calculate_percentage_of_unclassified_commits(self):
        if self.commits_amount == 0:
            return 0
        else:
            return sum(commit_message.commit_type == CommitMessagesTypes.UNCLASSIFIED for commit_message in
                       self.commit_messages) / self.commits_amount

    def _calculate_percentage_of_merge_pr_commits(self):
        if self.commits_amount == 0:
            return 0
        else:
            return sum(commit_message.commit_type == CommitMessagesTypes.MERGE_PR for commit_message in self.commit_messages) / self.commits_amount

    def _calculate_percentage_of_config_change_commits(self):
        if self.commits_amount == 0:
            return 0
        else:
            return sum(commit_message.commit_type == CommitMessagesTypes.CONFIG for commit_message in self.commit_messages) / self.commits_amount

    def _calculate_percentage_of_fix_commits(self):
        if self.commits_amount == 0:
            return 0
        else:
            return sum(commit_message.commit_type == CommitMessagesTypes.FIX for commit_message in self.commit_messages) / self.commits_amount

    def _calculate_percentage_of_feature_commits(self):
        if self.commits_amount == 0:
            return 0
        else:
            return sum(commit_message.commit_type == CommitMessagesTypes.FEATURE for commit_message in self.commit_messages) / self.commits_amount

    def _calculate_average_commit_message_fog_index(self):
        if self.commits_amount == 0:
            return 0
        else:
            return sum(commit_message.fog_index for commit_message in self.commit_messages) / self.commits_amount

    def _calculate_classified_to_unclassified_cm_ratio(self):
        if self.commits_amount == 0:
            return 0
        else:
            classified = sum(commit_message.commit_type != CommitMessagesTypes.UNCLASSIFIED for commit_message in
                             self.commit_messages)
            return classified / self.commits_amount


class CommitMessageAnalyzer:

    def __init__(self, message):
        self.message = message
        self.lower_cased_message = message.lower()
        self.message_length = len(message)
        self.words = self._extract_words()
        self.words_amount = len(self.words)
        self.fog_index = textstat.gunning_fog(message)
        self.commit_type = self._classify_commit_type()
        self.average_words_length = self._calculate_average_words_length()

    def _extract_words(self):
        raw_message = self.lower_cased_message
        # extract paths or urls
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = re.findall(url_pattern, raw_message)
        raw_message = re.sub(url_pattern, '', raw_message)

        path_pattern = re.compile(r'(/[^/ ]*)+|([a-zA-Z]:\\[\\\S|*\S]?.*)')
        paths = re.findall(path_pattern, raw_message)
        raw_message = re.sub(path_pattern, '', raw_message)

        url_path_list = urls + [path[0] for path in paths]
        # get rid of punctuation
        translator = str.maketrans('', '', string.punctuation.replace('-', ''))
        raw_message = raw_message.translate(translator)
        # extract the rest of words
        tokenized = TweetTokenizer().tokenize(raw_message)
        # return the words list
        tokenized.extend(url_path_list)
        return tokenized

    def _calculate_average_words_length(self):
        if self.words_amount == 0:
            return 0
        else:
            return sum(len(word) for word in self.words) / self.words_amount

    def _classify_commit_type(self):
        feature_keywords = ('feat', 'feature', 'add', 'added', 'implement', 'implemented', 'create', 'created',
                            'introduce', 'introduced', 'build', 'built', 'develop', 'developed', 'design', 'designed',
                            'enhance', 'enhanced', 'upgrade', 'upgraded', 'update', 'updated', 'extend', 'extended',
                            'improve', 'improved')
        fix_keywords = ('fix', 'fixed', 'fixes', 'repair', 'correct', 'resolve', 'resolved', 'debug',
                        'adjust', 'patch', 'solve', 'solved')
        merge_keywords = ('merge', 'pr', 'pull request')
        config_keywords = ('config', 'conf', 'configuration', 'settings', 'setup', 'yaml', 'json', 'xml', 'ini',
                           'cfg', 'param', 'parameter', 'option', 'adjustment', 'tweak')
        if any(keyword in self.words for keyword in merge_keywords):
            return CommitMessagesTypes.MERGE_PR
        if any(keyword in self.words for keyword in feature_keywords):
            return CommitMessagesTypes.FEATURE
        if any(keyword in self.words for keyword in fix_keywords):
            return CommitMessagesTypes.FIX
        if any(keyword in self.words for keyword in config_keywords):
            return CommitMessagesTypes.CONFIG
        return CommitMessagesTypes.UNCLASSIFIED
