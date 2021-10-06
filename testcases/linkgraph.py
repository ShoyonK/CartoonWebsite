# from selenium.common.exceptions import UnexpectedAlertPresentException
import os

from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException

import re


class LinkGraph:

    def __init__(self, driver):
        self.driver = driver
        self.nodes = []

    def load_from_file(self, file_path):
        self.nodes = []

        current_dir = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        file_full_path = current_dir + file_path
        with open(file_full_path, 'r') as f:
            lines = f.readlines()

        p = re.compile("LinkNode\((.+), (.+), (.*)\)")

        for line in lines:
            match = p.match(line)
            base_url = "http://127.0.0.1:5000" + match.group(1)
            dead = True if match.group(2) == "True" else False
            neighor_tags = match.group(3)

            node = self.get_node(base_url)

            if node is None:
                node = LinkNode(base_url)
                self.nodes.append(node)

            node.dead = dead

            if len(neighor_tags) > 0:
                list = neighor_tags.split(';')
                list = ["http://127.0.0.1:5000" + a for a in list]

                for url in list:
                    neighbor = self.get_node(url)

                    if neighbor is None:
                        neighbor = LinkNode(url)
                        self.nodes.append(neighbor)

                    node.neighbors.append(neighbor)
                    node.neighbor_urls.append(url)

    # this method takes a very long time
    def load_from_base_url(self, base_url, max_depth=4, freeze=False):
        self.nodes = []

        base_node = LinkNode(base_url)

        search_queue = [base_node]
        depth_queue = [0]
        visited = [base_node]

        while len(search_queue) > 0:
            current_node = search_queue.pop(0)
            current_depth = depth_queue.pop(0)

            print("now visiting (%d):" % current_depth, current_node.link_url)

            try:
                self.add_neighbors(current_node)

                if current_depth < max_depth - 1:
                    for neighbor in current_node.neighbors:
                        if neighbor not in visited:
                            search_queue.append(neighbor)
                            depth_queue.append(current_depth + 1)
                            visited.append(neighbor)

            except UnexpectedAlertPresentException:
                current_node.dead = True
                print("dead node:", current_node.link_url)

        if freeze:
            self.freeze()

    def get_nodes_of_depth(self, depth):
        base_node = self.nodes[0]
        search_queue = [base_node]
        depth_queue = [0]
        visited = [base_node]

        nodes = []

        while len(search_queue) > 0:
            current_node = search_queue.pop(0)
            current_depth = depth_queue.pop(0)

            if current_depth == depth:
                nodes.append(current_node)
            elif current_depth < depth:
                for neighbor in current_node.neighbors:
                    if neighbor not in visited:
                        search_queue.append(neighbor)
                        depth_queue.append(current_depth + 1)
                        visited.append(neighbor)

        return nodes

    def find_urls(self):
        driver = self.driver
        urls = []

        elements = driver.find_elements_by_partial_link_text('')

        for element in elements:
            element_url = element.get_attribute("href")

            if '#' not in element_url:
                urls.append(element_url)

        return urls

    def add_neighbors(self, link_node):
        driver = self.driver
        driver.get(link_node.link_url)

        urls = self.find_urls()

        for url in urls:
            if url not in link_node.neighbor_urls:
                neighbor = self.get_node(url)

                if neighbor is None:
                    neighbor = LinkNode(url)
                    self.nodes.append(neighbor)

                link_node.neighbors.append(neighbor)
                link_node.neighbor_urls.append(url)

        # pagination detection
        n = 2
        button = driver.find_elements_by_link_text(str(n))
        button = button[0] if button else None

        while button is not None:
            button.click()

            urls = self.find_urls()

            for url in urls:
                if url not in link_node.neighbor_urls:
                    neighbor = self.get_node(url)

                    if neighbor is None:
                        neighbor = LinkNode(url)
                        self.nodes.append(neighbor)

                    link_node.neighbors.append(neighbor)
                    link_node.neighbor_urls.append(url)

            n = n + 1
            button = driver.find_elements_by_link_text(str(n))
            button = button[0] if button else None

    def get_node(self, link_url):
        for node in self.nodes:
            if node.link_url == link_url:
                return node

        return None

    def freeze(self):
        with open("testcases/linkgraphdata.txt", 'w') as f:
            for item in self.nodes:
                value = repr(item)
                value = value.replace("http://127.0.0.1:5000", '')
                f.write("%s\n" % value)


class LinkNode:

    def __init__(self, link_url):
        self.dead = False
        self.link_url = link_url
        self.neighbors = []
        self.neighbor_urls = []

    def __repr__(self):
        return "LinkNode(%s, %s, %s)" % (self.link_url, self.dead, ";".join(self.neighbor_urls))
