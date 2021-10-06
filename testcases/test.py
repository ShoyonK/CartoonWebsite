import time
import random
import re

from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import chromedriver_binary
import unittest

from selenium.webdriver.support.select import Select

import testcases.linkgraph as linkgraph

# import all required frameworks
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# todo: several GUI changes have made some tests obsolete, so fix them


class WebsiteTest(unittest.TestCase):

    # initialization of webdriver
    def setUp(self):
        self.driver = webdriver.Chrome()

        self.web_graph = linkgraph.LinkGraph(self.driver)
        self.web_graph.load_from_file("\\linkgraphdata.txt")

        # print("there are", len(self.web_graph.nodes))

    def test_page_404(self):
        driver = self.driver
        web_graph = self.web_graph

        batch_size = 10

        nodes = web_graph.nodes.copy()
        random.shuffle(nodes)

        n = 0
        redirects = 0

        while n < batch_size:
            node = nodes[n]

            try:
                driver.get(node.link_url)

                assert "404" not in driver.title, \
                    "hit a 404 page"

            except UnexpectedAlertPresentException:
                redirects = redirects + 1

            n = n + 1

        print("batch size = %d, %d redirects" % (batch_size, redirects))

    def test_instance_links(self):
        driver = self.driver
        web_graph = self.web_graph

        batch_size = 10
        pass_threshold = 2

        # get all instances on depth 2 (from model page)
        nodes = web_graph.get_nodes_of_depth(2)
        random.shuffle(nodes)

        n = 0
        passed = 0
        p = re.compile("Go to (.+)'s")

        action_chains = ActionChains(driver)

        while passed < pass_threshold and n < batch_size:
            node = nodes[n]

            try:
                driver.get(node.link_url)

                elements = driver.find_elements_by_partial_link_text("Go to")

                if elements:
                    while len(elements) > 1:
                        elements.pop()

                for related_element in elements:

                    element_text = related_element.text
                    element_match = p.match(element_text)
                    related_element_text = element_match.group(1)

                    driver.get(related_element.get_attribute("href"))

                    title = driver.find_element_by_tag_name("h1").text
                    # some titles are in different languages, so we use a threshold value instead
                    # some pages also redirect

                    if related_element_text in title:
                        passed = passed + 1

                n = n + 1
            except UnexpectedAlertPresentException:
                print("redirect, testing another instance")

        assert passed == pass_threshold, \
            "passed %d, expected %d" % (passed, pass_threshold)

    def test_anime_instance_content_presence(self):
        driver = self.driver
        web_graph = self.web_graph

        batch_size = 10
        pass_threshold = 2

        # get all instances on depth 2 (from model page) and depth 3 (related instances)
        all_nodes = web_graph.get_nodes_of_depth(2)
        all_nodes.extend(web_graph.get_nodes_of_depth(3))

        # get only anime instances
        nodes = []

        for node in all_nodes:
            if "/animes/" in node.link_url:
                nodes.append(node)

        random.shuffle(nodes)

        fields = ["Description:", "Genres:", "Score:", "Start Date:", "Episodes:", "Type:", "Duration:", "Rating:",
                  "Currently Airing:"]

        passed = 0
        failed = 0

        n = 0

        while passed < pass_threshold and n < batch_size:
            node = nodes[n]

            try:
                check = True

                driver.get(node.link_url)
                action_chains = ActionChains(driver)

                for field in fields:
                    elements = driver.find_elements_by_xpath("//*[contains(text(), '%s')]" % (field))
                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                        break

                if check:
                    # trailer check

                    elements = driver.find_elements_by_tag_name("iframe")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                if check:
                    # thumbnail check for anime

                    elements = driver.find_elements_by_css_selector(".img-thumbnail.center-block")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                if check:
                    # title check

                    elements = driver.find_elements_by_tag_name("h1")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                if check:
                    # reviews check

                    elements = driver.find_elements_by_class_name("col-12")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                if check:
                    # carousel visibility check

                    elements = driver.find_elements_by_css_selector(".carousel-inner.w-100")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                # passed content presence checks

                if check:
                    passed = passed + 1
                else:
                    failed = failed + 1

            except UnexpectedAlertPresentException:
                failed = failed + 1

            n = n + 1

        print("passed %d, failed %d" % (passed, failed))

        assert passed == pass_threshold, \
            "passed %d elements, expected %d" % (passed, pass_threshold)

    def test_character_instance_content_presence(self):
        driver = self.driver
        web_graph = self.web_graph

        batch_size = 10
        pass_threshold = 2

        # get all instances on depth 2 (from model page) and depth 3 (related instances)
        all_nodes = web_graph.get_nodes_of_depth(2)
        all_nodes.extend(web_graph.get_nodes_of_depth(3))

        # get only character instances
        nodes = []

        for node in all_nodes:
            if "/characters/" in node.link_url:
                nodes.append(node)

        random.shuffle(nodes)

        fields = ["Description:"]

        passed = 0
        failed = 0

        n = 0

        while passed < pass_threshold and n < batch_size:
            node = nodes[n]

            try:
                check = True

                driver.get(node.link_url)
                action_chains = ActionChains(driver)

                for field in fields:
                    elements = driver.find_elements_by_xpath("//*[contains(text(), '%s')]" % (field))
                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                        break

                if check:
                    # thumbnail check for character

                    elements = driver.find_elements_by_css_selector(".img-thumbnail.center-block")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                if check:
                    # title check

                    elements = driver.find_elements_by_tag_name("h1")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                if check:
                    # carousel visibility check

                    elements = driver.find_elements_by_css_selector(".carousel-inner.w-100")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                # passed content presence checks

                if check:
                    passed = passed + 1
                else:
                    failed = failed + 1

            except UnexpectedAlertPresentException:
                failed = failed + 1

            n = n + 1

        print("passed %d, failed %d" % (passed, failed))

        assert passed == pass_threshold, \
            "passed %d elements, expected %d" % (passed, pass_threshold)

    def test_staff_instance_content_presence(self):
        driver = self.driver
        web_graph = self.web_graph

        batch_size = 10
        pass_threshold = 2

        # get all instances on depth 2 (from model page) and depth 3 (related instances)
        all_nodes = web_graph.get_nodes_of_depth(2)
        all_nodes.extend(web_graph.get_nodes_of_depth(3))

        # get only character instances
        nodes = []

        for node in all_nodes:
            if "/staff/" in node.link_url:
                nodes.append(node)

        random.shuffle(nodes)

        fields = ["Description:", "Date of Birth:"]

        passed = 0
        failed = 0

        n = 0

        while passed < pass_threshold and n < batch_size:
            node = nodes[n]

            try:
                check = True

                driver.get(node.link_url)
                action_chains = ActionChains(driver)

                for field in fields:
                    elements = driver.find_elements_by_xpath("//*[contains(text(), '%s')]" % (field + ' '))
                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                        break

                if check:
                    # thumbnail check for staff

                    elements = driver.find_elements_by_css_selector(".img-thumbnail.center-block")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                if check:
                    # title check

                    elements = driver.find_elements_by_tag_name("h1")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                if check:
                    # double carousel visibility check

                    elements = driver.find_elements_by_css_selector(".carousel-inner.w-100")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    element1 = elements[0].is_displayed() if elements else False

                    if elements:
                        action_chains.move_to_element(elements[1]).perform()

                    element2 = elements[1].is_displayed() if elements else False

                    if not element1 or not element2:
                        check = False

                # passed content presence checks

                if check:
                    passed = passed + 1
                else:
                    failed = failed + 1

            except UnexpectedAlertPresentException:
                failed = failed + 1

            n = n + 1

        print("passed %d, failed %d" % (passed, failed))

        assert passed == pass_threshold, \
            "passed %d elements, expected %d" % (passed, pass_threshold)

    def test_studio_instance_content_presence(self):
        driver = self.driver
        web_graph = self.web_graph

        batch_size = 10
        pass_threshold = 2

        # get all instances on depth 2 (from model page) and depth 3 (related instances)
        all_nodes = web_graph.get_nodes_of_depth(2)
        all_nodes.extend(web_graph.get_nodes_of_depth(3))

        # get only studio instances
        nodes = []

        for node in all_nodes:
            if "/studios/" in node.link_url:
                nodes.append(node)

        random.shuffle(nodes)

        fields = ["Description:"]

        passed = 0
        failed = 0

        n = 0

        while passed < pass_threshold and n < batch_size:
            node = nodes[n]

            try:
                check = True

                driver.get(node.link_url)
                action_chains = ActionChains(driver)

                for field in fields:
                    elements = driver.find_elements_by_xpath("//*[contains(text(), '%s')]" % (field + ' '))
                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                        break

                if check:
                    # thumbnail check for studio

                    elements = driver.find_elements_by_css_selector(".img-thumbnail.center-block")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                if check:
                    # title check

                    elements = driver.find_elements_by_tag_name("h1")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                if check:
                    # carousel visibility check

                    elements = driver.find_elements_by_css_selector(".carousel-inner.w-100")

                    if elements:
                        action_chains.move_to_element(elements[0]).perform()

                    elements = elements[0].is_displayed() if elements else False

                    if not elements:
                        check = False

                # passed content presence checks

                if check:
                    passed = passed + 1
                else:
                    failed = failed + 1

            except UnexpectedAlertPresentException:
                failed = failed + 1

            n = n + 1

        print("passed %d, failed %d" % (passed, failed))

        assert passed == pass_threshold, \
            "passed %d elements, expected %d" % (passed, pass_threshold)

    def test_model_pagination(self):
        urls = ["http://127.0.0.1:5000/animes", "http://127.0.0.1:5000/characters", "http://127.0.0.1:5000/staff",
                "http://127.0.0.1:5000/studios"]

        driver = self.driver

        for url in urls:
            driver.get(url)

            n = 1
            button = driver.find_elements_by_link_text(str(n))
            button = button[0] if button else None

            while button is not None:
                button.click()

                # make sure button is active
                button_parent = button.find_element_by_xpath("./..")

                assert "active" in button_parent.get_attribute("class"), \
                    "pagination button failed to highlight"

                # make sure at least one card is visible

                all_cards = driver.find_elements_by_class_name("card-body")
                visible_cards = []

                for card in all_cards:
                    if card.is_displayed():
                        visible_cards.append(card)

                assert len(visible_cards) > 0, \
                    "no cards visible on page %d in url %s" % (n, url)

                n = n + 1
                button = driver.find_elements_by_link_text(str(n))
                button = button[0] if button else None

    def test_model_page_search_bar(self):
        driver = self.driver

        model_page_urls = ["http://127.0.0.1:5000/animes", "http://127.0.0.1:5000/characters",
                           "http://127.0.0.1:5000/staff"]

        for model_page_url in model_page_urls:
            driver.get(model_page_url)

            search_terms = ["abcdef", "abc def", "abc.def", "abc/def", "abc+def", "abc_def", "abc&def", "abc=def",
                            "abc:def", "abc!def", "abc*def"]

            for search_term in search_terms:
                search_bar_input = driver.find_element_by_css_selector("input[name='search_string']")
                search_bar_submit = driver.find_element_by_css_selector("input[value*='Search']")

                search_bar_input.clear()
                search_bar_input.send_keys(search_term)
                search_bar_submit.click()

                # when render_template is called, the search bar will contain the actual search text
                actual_search_term = driver.find_element_by_css_selector("input[name='search_string']").get_attribute(
                    "value")

                assert actual_search_term.lower() == search_term.lower(), \
                    "Search bar failed to display correct query"

    def test_model_page_searching(self):
        driver = self.driver

        model_page_urls = ["http://127.0.0.1:5000/animes", "http://127.0.0.1:5000/characters",
                           "http://127.0.0.1:5000/staff"]
        model_page_search_terms = [
            ["naruto", "naru", "academia", "hero aca", "childhood friend"],
            ["naruto", "sasu", "a boy"],
            ["kana", "yuuki kaji", "when he was"]
        ]

        for i in range(len(model_page_urls)):
            model_page_url = model_page_urls[i]
            search_terms = model_page_search_terms[i]

            for search_term in search_terms:
                if driver.current_url != model_page_url:
                    driver.get(model_page_url)

                search_bar_input = driver.find_element_by_css_selector("input[name='search_string']")
                search_bar_submit = driver.find_element_by_css_selector("input[value*='Search']")

                search_bar_input.clear()
                search_bar_input.send_keys(search_term)
                search_bar_submit.click()

                instances = driver.find_elements_by_class_name("card-body")
                instance_info = []

                for instance in instances:
                    info = dict()
                    card_title = instance.find_element_by_class_name("card-title")
                    info["title"] = card_title.text
                    info["link"] = instance.find_element_by_tag_name("a").get_attribute("href")

                    instance_info.append(info)

                for info in instance_info:
                    contains = search_term.lower() in info["title"].lower()

                    if not contains:
                        driver.get(info["link"])

                        instance_body = driver.find_element_by_tag_name("body")
                        contains = search_term.lower() in instance_body.get_attribute("innerHTML").lower()

                    assert contains, \
                        "Unrelated result for search term %s" % search_term

    def test_model_page_filtering(self):
        # only for anime since other filters are not yet completed

        driver = self.driver
        driver.get("http://127.0.0.1:5000/animes")

        search_bar_submit = driver.find_element_by_css_selector("input[value*='Search']")
        sort_input = driver.find_element_by_css_selector("select[name='sort']")
        sort_selector = Select(sort_input)

        driver.execute_script("javascript:document.getElementById(\"myRange\").value=70")

        sort_selector.select_by_visible_text("Score Increasing")
        search_bar_submit.click()

        first_card = driver.find_element_by_class_name("card-body")

        list_items = first_card.find_elements_by_class_name("list-group-item")
        card_score = False

        pattern = re.compile("Score: (\d+)")

        for list_item in list_items:
            result = pattern.match(list_item.get_attribute("innerHTML"))

            if result is not None:
                card_score = int(result.group(1))
                break

        assert card_score, "Failed to find anime score"
        assert card_score <= 70, "Filter failed to ignore score lower than 70: %d" % card_score

    def test_model_page_sorting(self):
        driver = self.driver

        model_page_urls = ["http://127.0.0.1:5000/animes", "http://127.0.0.1:5000/characters",
                           "http://127.0.0.1:5000/staff"]
        model_page_sorts = [
            ["Alphabetical", "Reverse Alphabetical"],
            ["Alphabetical", "Reverse Alphabetical"],
            ["Alphabetical", "Reverse Alphabetical"]
        ]

        for i in range(len(model_page_urls)):
            model_page_url = model_page_urls[i]
            sort_methods = model_page_sorts[i]

            driver.get(model_page_url)

            for sort_method in sort_methods:
                search_bar_submit = driver.find_element_by_css_selector("input[value*='Search']")
                sort_input = driver.find_element_by_css_selector("select[name='sort']")
                sort_selector = Select(sort_input)

                sort_selector.select_by_visible_text(sort_method)
                search_bar_submit.click()

                instances = []

                for instance in driver.find_elements_by_class_name("card-body"):
                    if instance.is_displayed():
                        instances.append(instance)

                assert len(instances) != 0, \
                    "Failed to sort with %s" % sort_method

                for j in range(len(instances) - 1):
                    current_instance = instances[j]
                    next_instance = instances[j + 1]

                    # as of 11/19, sorting is case sensitive
                    current_value = current_instance.find_element_by_class_name("card-title").text
                    next_value = next_instance.find_element_by_class_name("card-title").text

                    if sort_method == "Alphabetical":
                        assert current_value <= next_value, \
                            "Invalid sorting for %s: %s and %s" % (sort_method, current_value, next_value)
                    elif sort_method == "Reverse Alphabetical":
                        assert current_value >= next_value, \
                            "Invalid sorting for %s: %s and %s" % (sort_method, current_value, next_value)

    def test_text_scroll_in_splash_page(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")

        # preload time
        # time.sleep(5)

        # splash text that should be visible
        scroll_text = ["Welcome Anime Fans!", "To", "The Ultimate Anime Database", "by Team E14"]

        # locate elements using text
        text_elements = []

        # series of opacity values we must pass through (True means visible, False means invisible) to pass
        opacity_checkpoints = [
            # initially, only first text element is visible
            [True, False, False, False],

            # at max opacity, all elements should be fully visible
            [True, True, True, True],

            # at min opacity, no elements should be visible
            [False, False, False, False]
        ]

        # checkpoint values, we must pass through these sequentially before we reach the end to pass
        validation = [False, False, False]

        # get the text elements
        for text in scroll_text:
            text_element = driver.find_element_by_xpath("//*[contains(text(), '%s')]" % text)
            text_elements.append(text_element)

        # store last scroll position
        last_scroll_pos = driver.execute_script("return window.pageYOffset;")

        # scroll through the page, making sure opacity fades correctly
        while True:
            time.sleep(0.1)
            driver.execute_script("window.scrollBy(0, 50);")

            # store opacity values
            opacity_values = []

            for text_element in text_elements:
                opacity_values.append(float(text_element.value_of_css_property("opacity")) > 0)

            # update validation checkpoints
            for i in range(3):
                opacity_checkpoint = opacity_checkpoints[i]

                if opacity_values == opacity_checkpoint:
                    validation[i] = True

            # validation should go from: TFF to TTF to TTT
            # print("VALIDATION:", validation[0], validation[1], validation[2])

            # now make sure we sequentially passed through our other checkpoints
            for i in range(1, 3):
                passed = validation[i]

                if passed:
                    for j in range(i):
                        assert validation[j], \
                            "Failed to fade elements in order"

            # if we are at the bottom of the page, and we haven't finished validation, we fail
            new_scroll_pos = driver.execute_script("return window.pageYOffset;")

            if new_scroll_pos == last_scroll_pos:
                assert validation[2], \
                    "Failed to fade elements in order before reaching end of page"
                break

            last_scroll_pos = new_scroll_pos

    # cleanup method called after every test performed
    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
