import typing
import requests
import urllib.parse
import os

# Selenium Imports
from selenium.webdriver import ActionChains, Chrome, ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys


class GoogleImageExtractor:
    # for selenium
    webdriver_bin_path = "webdriver"+os.sep+"chromedriver.exe"
    # for Google Images
    __google_images_url = "https://www.google.com/search?"
    __url_data = {"tbm" : "isch", "source" : "lmns", "hl" : "en"}

    # extensions to download
    allowed_extensions : list = ["png", "gif", "jpg", "jpeg", "webp", "bmp", "svg", "ico"]

    # Private Methods (intended : Python doesn't have access modifiers)

    def __init__(self, search_query : str, number_of_images : int = 10, destination_folder : str = os.curdir, url_only : bool = False) -> None:
        self.__search_query = search_query
        self.__number_of_images = number_of_images
        self.__destination_folder = destination_folder
        self.__url_only = url_only

        #set values
        self.__url_data['q'] = self.__search_query

    def __get_file_name_ext(self, url : str) -> typing.Tuple[str, str]:
        name, ext = os.path.splitext(os.path.basename(urllib.parse.urlparse(url).path))

        file_name = self.__get_sanitized_filename(name)
        file_ext = ext[1:] #remove dot

        # if can't find extension then try finding it from url headers
        headers = requests.head(url).headers
        file_ext = headers['content-type'].split(';')[0].split('/')[-1] if 'content-type' in headers else ""

        return file_name, file_ext

    def __download_images(self, urls : list) -> None:
        for url in urls:
            file_name, file_ext = self.__get_file_name_ext(url)
            
            # download file
            if file_ext in self.allowed_extensions:
                content = requests.get(url).content
                file_path = self.__get_unique_filepath(self.__destination_folder, file_name, file_ext)

                with open(file_path, "wb") as fh:
                    fh.write(content)
                    fh.close()

    def __write_urls_to_file(self, image_urls) -> None:
        file_name = self.__search_query[:20] if len(self.__search_query) > 20 else self.__search_query
        file_ext = "log"
        log_file_path = self.__get_unique_filepath(self.__destination_folder, file_name, file_ext)
        
        with open(log_file_path, "w") as fh:
            fh.write(os.linesep.join(image_urls))
            fh.close()
    
    @staticmethod
    def __get_sanitized_filename(file_name, default_name="file") -> str:
        if len(file_name) == 0:
            return default_name
        return "".join(i for i in file_name if i not in "\/:*?<>|")

    @staticmethod
    def __get_unique_filepath(folder_name, file_name, file_ext) -> str:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        new_file_name = file_name
        counter = 1
        while os.path.exists(folder_name+os.sep+new_file_name+os.extsep+file_ext):
            new_file_name = file_name + f" ({counter})"
            counter += 1
        
        return folder_name+os.sep+new_file_name+os.extsep+file_ext

    def __generate_url(self) -> str:
        # do not encode colon (:) as %3A
        url = self.__google_images_url+urllib.parse.urlencode(self.__url_data).replace("%3A", ":")
        
        return url

    def __get_webdriver(self) -> WebDriver:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) #logging off

        driver = Chrome(executable_path=self.webdriver_bin_path, options=chrome_options)
        
        return driver
    
    def __extract_urls(self) -> list:
        driver = self.__get_webdriver()
        driver.get(self.__generate_url())

        # img urls 
        img_urls = []
    
        #selectors
        sel_a_tags = 'a.wXeWr.islib.nfEiy.mM5pbd' #<a> containing <img> and loads original image url in href
        sel_status_div = 'div.DwpMZe' #end div
        sel_loadmore_btn = 'input.mye4qd' #Show more results

        a_tags = driver.find_elements_by_css_selector(sel_a_tags)
        while self.__number_of_images > len(a_tags):
            status_div = driver.find_element_by_css_selector(sel_status_div)
            status = int(status_div.get_attribute('data-status'))
            loadmore_btn = driver.find_element_by_css_selector(sel_loadmore_btn)

            #status 1 : wait, 5:wait/new content, 3:reached end
			#scroll available
            if not loadmore_btn.is_displayed() and (status == 1 or status == 5):
                driver.find_element_by_css_selector('body').send_keys(Keys.END)

            #load-more button available
            elif loadmore_btn.is_displayed():
                ActionChains(driver).move_to_element(loadmore_btn).click().perform()

			#reached end 
            # NOT NECCESSARY
            # elif status == 3:
            #     break

            #something else
            else:
                break

            a_tags = driver.find_elements_by_css_selector(sel_a_tags)
        
        for tag in a_tags[:self.__number_of_images]:
            ActionChains(driver).move_to_element(tag).context_click().perform()

            queries = tag.get_attribute('href').split('?')[1].split('&')

            for q in queries:
                chunks = q.split('=')

                if urllib.parse.unquote(chunks[0]) == 'imgurl':
                    img_urls.append(urllib.parse.unquote(chunks[1]))
                    break
        
        driver.quit()

        return img_urls

    # Following methods are intended to be public

    def run(self) -> None:
        if self.__number_of_images > 0:
            image_urls = self.__extract_urls()

            if self.__url_only:
                self.__write_urls_to_file(image_urls)
            else:
                self.__download_images(image_urls)
   
    def apply_safesearch(self, safe : bool = True) -> None:
        self.__url_data['safe'] = "active" if safe == True else "images"

    def apply_search_filters(self, size : str = "any", color : str = "any", type : str = "any", time : str = "any", license : str = "any") -> None:
        filters = {
            # size
            "isz" : {
                "large" : "l",
                "medium" : "m",
                "icon" : "i"
            }, 

            #color
            "ic" : {
                "black and white" : "gray",
                "transparent" : "trans",
                "red" : "specific,isc:red",
                "orange" : "specific,isc:orange",
                "yellow" : "specific,isc:yellow",
                "green" : "specific,isc:green",
                "teal" : "specific,isc:teal",
                "blue" : "specific,isc:blue",
                "purple" : "specific,isc:purple",
                "pink" : "specific,isc:pink",
                "white" : "specific,isc:white",
                "gray" : "specific,isc:gray",
                "black" : "specific,isc:black",
                "brown" : "specific,isc:brown"
            },

            # type
            "itp" : {
                "clip art" : "clipart",
                "line drawing" : "lineart",
                "gif" : "animated"
            },

            # time
            "qdr" : {
                "past 24 hours" : "d",
                "past week" : "w",
                "past month" : "m",
                "past year" : "y"
            }, 

            # Usage Rights
            "il" : {
                "creative commons licenses" : "cl",
                "commercial & other licenses" : "ol"
            }
        }
        args = {"isz" : size.lower(), "ic" : color.lower(), "itp" : type.lower(), "qdr" : time.lower(), "il" : license.lower()}
        filter_query = []

        for key, val in args.items():
            if val in filters[key]:
                filter_query.append(key+":"+filters[key][val])

        self.__url_data['tbs'] = ",".join(filter_query)
