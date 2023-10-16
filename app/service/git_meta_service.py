""" import re
import requests
from json import dumps
from json.decoder import JSONDecodeError

from requests import Response
from bs4 import BeautifulSoup
from json import loads

class GitHubMetadataService:
    REPOSITORIES_PATTERN = re.compile("codeRepository[^\\s]+[^\\S][^\\n][^\\S]+([^<]+)")
    NUM_OF_REPOSITORIES_PATTERN = re.compile("Repositories[^<]+<span title=\\\"([^\\\"]+)")
    NAME_PATTERN = re.compile("itemprop=\\\"name[^\\s]+[^\\S][^\\n][^\\S]+([^\\n]+)")
    FOLLOWERS_PATTERN = re.compile("class=\\\"text-bold color-fg-default\\\">([^<]+)[^\\d]+follower")
    FOLLOWING_PATTERN = re.compile("fg-default\\\">([^<]+)[^]d]+\\bfollowing\\b")
    FORKS_PATTERN1 = re.compile("text-bold[^>]+>([^<]+)[^f]+forks")
    FORKS_PATTERN2 = re.compile("</svg>Fork[^C]+[^\\d]+([^<]+)")
    STARS_PATTERN1 = re.compile("text-bold[^>]+>([^<]+)[^f]+stars")
    STARS_PATTERN2 = re.compile("repo-stars-counter-star[^=]+=\\\"([^ ]+)")
    COMMITS_PATTERN = re.compile("<span class=\\\"d-none d-sm-inline\\\">[^\\S]+<strong>([^<]+)")
    PROGRAMMING_LANGUAGE_PATTERN = re.compile("programmingLanguage\\\">([^<]+)")
    FORKED_FROM_PATTERN = re.compile("forked[ ]from([^h]+)")
    EMPTY_PATTERN = re.compile("This repository is ([^.]+)")
    USER_NOT_FOUND_PATTERN = re.compile("This is not the ([^ ]+)")

    def __init__(self):
        self.producer = Producer()
        self.userRepositoryCountService = UserRepositoryCountService()
        self.client = requests.session()
        self.client.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
        self.client.get("https://github.com/")
        
    def get_metadata(self, username):
        object_node = self.metadata(username)

        if object_node.get("USER_NOT_FOUND"):
            return None
        
        self.userRepositoryCountService.set_user_repository_count(username, 0)

        object_node = self.repositories_data(username, object_node.get("public_repos"))
        self.producer.send(object_node.get("repositoriesUrls"))

        ret_str = object_node.get("repositoriesUrls")
        object_node.pop("repositoriesUrls")

        ret_json = dumps({"results": ret_str})
        ret_json_node = loads(ret_json)

        return ret_json_node

    def metadata(self, username):
        html = self.get_repositories_page_html(username, 1)
        object_node = dict()

        user_not_found = self.get_regex_group(self.USER_NOT_FOUND_PATTERN, html, "", username)
        if user_not_found == "USER_NOT_FOUND":
            object_node["USER_NOT_FOUND"] = True
            return object_node
        else:
            object_node["USER_NOT_FOUND"] = False

        object_node["name"] = self.get_regex_group(self.NAME_PATTERN, html, "Name", username)
        if object_node["name"] == "</span>":
            object_node["name"] = "N/A"
        object_node["username"] = username
        object_node["url"] = "https://github.com/" + username
        object_node["public_repos"] = self.get_regex_group(self.NUM_OF_REPOSITORIES_PATTERN, html, "Number of Repositories", username)
        object_node["followers"] = self.get_regex_group(self.FOLLOWERS_PATTERN, html, "Followers", username)
        object_node["following"] = self.get_regex_group(self.FOLLOWING_PATTERN, html, "Following", username)

        return object_node

    def repositories_data(self, username, public_repos):
        object_node = dict()
        matcher = re.compile(self.PROGRAMMING_LANGUAGE_PATTERN).finditer("text")

        programming_languages = {
            "SCSS": 0, "Assembly": 0, "Pawn": 0, "Objective-C": 0, "Dart": 0, "TypeScript": 0,
            "C": 0, "Kotlin": 0, "HTML": 0, "Java": 0, "EJS": 0, "C#": 0, "JavaScript": 0,
            "Jupyter Notebook": 0, "C++": 0, "CSS": 0, "Python": 0, "Node.js": 0, "Angular": 0,
            "React": 0, ".NET": 0, "PHP": 0, "Ruby": 0, "Scala": 0, "Swift": 0, "Go": 0,
            "Rust": 0, "R": 0
        }
        for i in range(1, int(public_repos) / 30 + 1):
            html = self.get_repositories_page_html(username, i)

            for match in matcher:
                lang = match.group(1)
                if lang in programming_languages:
                    programming_languages[lang] += 1

            repositories, forked_repositories, empty_repositories = self.get_repositories_info(html, username)

            object_node.update(repositories)
            object_node.update(forked_repositories)
            object_node.update(empty_repositories)

        object_node["repositoriesUrls"] = valid_repositories

        return object_node

    def get_repositories_info(self, html, username):
        matcher = re.compile(self.REPOSITORIES_PATTERN).finditer(html)
        valid_repositories = []
        forks = 0
        commits = 0
        stars = 0
        empty_repositories = 0
        forked_repositories = 0

        for match in matcher:
            URL = f"https://github.com/{username}/{match.group(1)}.git"

            try:
                is_empty, is_forked, repo_html = self.get_repository_html(URL)

                if is_empty:
                    empty_repositories += 1
                elif is_forked:
                    forked_repositories += 1
                else:
                    valid_repositories.append(URL)
                    forks += int(self.get_regex_group(self.FORKS_PATTERN1, repo_html, URL, username))
                    commits += int(self.get_regex_group(self.COMMITS_PATTERN, repo_html, URL, username))
                    stars += int(self.get_regex_group(self.STARS_PATTERN1, repo_html, URL, username))
            except:
                continue

        return {
            "forks": forks,
            "commits": commits,
            "stars": stars,
            "forked_repos": forked_repositories,
            "empty_repos": empty_repositories,
            "repositoriesUrls": valid_repositories
        }

    def get_repository_html(self, url):
        response = self.client.get(url)
        response.raise_for_status()
        return response.text

    def get_repositories_page_html(self, username, page_number):
        url = f"https://github.com/{username}?page={page_number}&tab=repositories"
        response = self.client.get(url)
        response.raise_for_status()
        return response.text

    def get_regex_group(self, pattern, html, source, username):
        match = re.search(pattern, html)
        
        try:
            ret = match.group(1)
            
            if pattern == self.USER_NOT_FOUND_PATTERN:
                return "USER_NOT_FOUND"

            if ret.endswith("k"):
                ret = self.convert_to_number(ret)

            if "," in ret:
                ret = ret.replace(",", "")

            return ret
        except:
            if pattern == self.USER_NOT_FOUND_PATTERN:
                return "USER_FOUND"

            if pattern == self.FORKS_PATTERN1:
                return self.get_regex_group(self.FORKS_PATTERN2, html, source, username)

            if pattern == self.STARS_PATTERN1:
                return self.get_regex_group(self.STARS_PATTERN2, html, source, username)

            if pattern == self.FORKED_FROM_PATTERN or pattern == self.EMPTY_PATTERN:
                return "0"

        return "0"

    @staticmethod
    def convert_to_number(s):
        num = float(s[:-1])
        return str(int(num * 1000)) """