#!/usr/bin/env python
# In[ ]:
#  coding: utf-8

###### Searching and Downloading Google Images to the local disk ######


import codecs
import datetime
import http.client
import json
import os
import re
import ssl
import sys
import time  # Importing the time library to check the time of code execution
import urllib.request
from http.client import BadStatusLine
from urllib.parse import quote
from urllib.request import HTTPError, Request, URLError, urlopen

# Import Libraries
from .. import LOGS
from .tools import async_searcher

http.client._MAXHEADERS = 1000

args_list = [
    "keywords",
    "keywords_from_file",
    "prefix_keywords",
    "suffix_keywords",
    "limit",
    "format",
    "color",
    "color_type",
    "usage_rights",
    "size",
    "exact_size",
    "aspect_ratio",
    "type",
    "time",
    "time_range",
    "delay",
    "url",
    "single_image",
    "output_directory",
    "image_directory",
    "no_directory",
    "proxy",
    "similar_images",
    "specific_site",
    "metadata",
    "extract_metadata",
    "socket_timeout",
    "thumbnail",
    "thumbnail_only",
    "language",
    "prefix",
    "chromedriver",
    "related_images",
    "safe_search",
    "no_numbering",
    "offset",
    "no_download",
    "save_source",
    "ignore_urls",
]


class googleimagesdownload:
    def __init__(self):
        pass

    # Downloading entire Web Document (Raw Page Content)
    async def download_page(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
            }

            # req = urllib.request.Request(url, headers=headers)
            # resp = urllib.request.urlopen(req)
            # return str(resp.read())
            resp = await async_searcher(url, re_content=True, headers=headers)
            return str(resp)
        except Exception as er:
            LOGS.exception(
                "Could not open URL. Please check your internet connection and/or ssl settings \n"
                "If you are using proxy, make sure your proxy settings is configured correctly"
            )
            raise er

    # Download Page for more than 100 images

    def download_extended_page(self, url, chromedriver):
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")

        try:
            browser = webdriver.Chrome(chromedriver, chrome_options=options)
        except Exception as e:
            LOGS.info(
                "Looks like we cannot locate the path the 'chromedriver' (use the '--chromedriver' "
                "argument to specify the path to the executable.) or google chrome browser is not "
                "installed on your machine (exception: %s)" % e
            )
            sys.exit()
        browser.set_window_size(1024, 768)

        # Open the link
        browser.get(url)
        time.sleep(1)

        element = browser.find_element_by_tag_name("body")
        # Scroll down
        for i in range(30):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

        try:
            browser.find_element_by_id("smb").click()
            for _ in range(50):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)  # bot id protection
        except BaseException:
            for _ in range(10):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)  # bot id protection

        time.sleep(0.5)

        source = browser.page_source  # page source
        # close the browser
        browser.close()

        return source

    # Correcting the escape characters for python2

    def replace_with_byte(self, match):
        return chr(int(match.group(0)[1:], 8))

    def repair(self, brokenjson):
        # up to 3 digits for byte values up to FF
        invalid_escape = re.compile(r"\\[0-7]{1,3}")
        return invalid_escape.sub(self.replace_with_byte, brokenjson)

    # Finding 'Next Image' from the given raw page

    def get_next_tab(self, s):
        start_line = s.find('class="dtviD"')
        if start_line == -1:  # If no links are found then give an error!
            end_quote = 0
            link = "no_tabs"
            return link, "", end_quote
        start_line = s.find('class="dtviD"')
        start_content = s.find('href="', start_line + 1)
        end_content = s.find('">', start_content + 1)
        url_item = "https://www.google.com" + str(s[start_content + 6 : end_content])
        url_item = url_item.replace("&amp;", "&")
        start_line_2 = s.find('class="dtviD"')
        s = s.replace("&amp;", "&")
        start_content_2 = s.find(":", start_line_2 + 1)
        end_content_2 = s.find("&usg=", start_content_2 + 1)
        url_item_name = str(s[start_content_2 + 1 : end_content_2])
        chars = url_item_name.find(",g_1:")
        chars_end = url_item_name.find(":", chars + 6)
        if chars_end == -1:
            updated_item_name = (url_item_name[chars + 5 :]).replace("+", " ")
        else:
            updated_item_name = (url_item_name[chars + 5 : chars_end]).replace("+", " ")
        return url_item, updated_item_name, end_content

    # Getting all links with the help of '_images_get_next_image'

    def get_all_tabs(self, page):
        tabs = {}
        while True:
            item, item_name, end_content = self.get_next_tab(page)
            if item == "no_tabs":
                break
            if len(item_name) > 100 or item_name == "background-color":
                break
            # Append all the links in the list named 'Links'
            tabs[item_name] = item
            # Timer could be used to slow down the request for image
            # downloads
            time.sleep(0.1)
            page = page[end_content:]
        return tabs

    # Format the object in readable format

    def format_object(self, object):
        data = object[1]
        main = data[3]
        info = data[9]
        return {
            "image_height": main[2],
            "image_width": main[1],
            "image_link": main[0],
            "image_format": main[0][-1 * (len(main[0]) - main[0].rfind(".") - 1) :],
            "image_description": info["2003"][3],
            "image_source": info["2003"][2],
            "image_thumbnail_url": data[2][0],
        }

    # function to download single image

    def single_image(self, image_url):
        main_directory = "downloads"
        extensions = (".jpg", ".gif", ".png", ".bmp", ".svg", ".webp", ".ico")
        url = image_url
        try:
            os.makedirs(main_directory)
        except OSError as e:
            if e.errno != 17:
                raise
        req = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            },
        )

        response = urlopen(req, None, 10)
        data = response.read()
        response.close()

        image_name = str(url[(url.rfind("/")) + 1 :])
        if "?" in image_name:
            image_name = image_name[: image_name.find("?")]
        # if ".jpg" in image_name or ".gif" in image_name or ".png" in
        # image_name or ".bmp" in image_name or ".svg" in image_name or ".webp"
        # in image_name or ".ico" in image_name:
        if any(map(lambda extension: extension in image_name, extensions)):
            file_name = main_directory + "/" + image_name
        else:
            file_name = main_directory + "/" + image_name + ".jpg"
            image_name = image_name + ".jpg"

        try:
            with open(file_name, "wb") as output_file:
                output_file.write(data)
        except IOError as e:
            raise e
        except OSError as e:
            raise e

    def similar_images(self, similar_images):
        try:
            searchUrl = (
                "https://www.google.com/searchbyimage?site=search&sa=X&image_url="
                + similar_images
            )
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            }

            req1 = urllib.request.Request(searchUrl, headers=headers)
            resp1 = urllib.request.urlopen(req1)
            content = str(resp1.read())
            l1 = content.find("AMhZZ")
            l2 = content.find("&", l1)
            urll = content[l1:l2]

            newurl = (
                "https://www.google.com/search?tbs=sbi:" + urll + "&site=search&sa=X"
            )
            req2 = urllib.request.Request(newurl, headers=headers)
            urllib.request.urlopen(req2)
            l3 = content.find("/search?sa=X&amp;q=")
            l4 = content.find(";", l3 + 19)
            return content[l3 + 19 : l4]
        except BaseException:
            return "Cloud not connect to Google Images endpoint"

    # Building URL parameters
    def build_url_parameters(self, arguments):
        if arguments["language"]:
            lang = "&lr="
            lang_param = {
                "Arabic": "lang_ar",
                "Chinese (Simplified)": "lang_zh-CN",
                "Chinese (Traditional)": "lang_zh-TW",
                "Czech": "lang_cs",
                "Danish": "lang_da",
                "Dutch": "lang_nl",
                "English": "lang_en",
                "Estonian": "lang_et",
                "Finnish": "lang_fi",
                "French": "lang_fr",
                "German": "lang_de",
                "Greek": "lang_el",
                "Hebrew": "lang_iw ",
                "Hungarian": "lang_hu",
                "Icelandic": "lang_is",
                "Italian": "lang_it",
                "Japanese": "lang_ja",
                "Korean": "lang_ko",
                "Latvian": "lang_lv",
                "Lithuanian": "lang_lt",
                "Norwegian": "lang_no",
                "Portuguese": "lang_pt",
                "Polish": "lang_pl",
                "Romanian": "lang_ro",
                "Russian": "lang_ru",
                "Spanish": "lang_es",
                "Swedish": "lang_sv",
                "Turkish": "lang_tr",
            }
            lang_url = lang + lang_param[arguments["language"]]
        else:
            lang_url = ""

        if arguments["time_range"]:
            json_acceptable_string = arguments["time_range"].replace("'", '"')
            d = json.loads(json_acceptable_string)
            time_range = ",cdr:1,cd_min:" + d["time_min"] + ",cd_max:" + d["time_max"]
        else:
            time_range = ""

        if arguments["exact_size"]:
            size_array = [x.strip() for x in arguments["exact_size"].split(",")]
            exact_size = (
                ",isz:ex,iszw:" + str(size_array[0]) + ",iszh:" + str(size_array[1])
            )
        else:
            exact_size = ""

        built_url = "&tbs="
        counter = 0
        params = {
            "color": [
                arguments["color"],
                {
                    "red": "ic:specific,isc:red",
                    "orange": "ic:specific,isc:orange",
                    "yellow": "ic:specific,isc:yellow",
                    "green": "ic:specific,isc:green",
                    "teal": "ic:specific,isc:teel",
                    "blue": "ic:specific,isc:blue",
                    "purple": "ic:specific,isc:purple",
                    "pink": "ic:specific,isc:pink",
                    "white": "ic:specific,isc:white",
                    "gray": "ic:specific,isc:gray",
                    "black": "ic:specific,isc:black",
                    "brown": "ic:specific,isc:brown",
                },
            ],
            "color_type": [
                arguments["color_type"],
                {
                    "full-color": "ic:color",
                    "black-and-white": "ic:gray",
                    "transparent": "ic:trans",
                },
            ],
            "usage_rights": [
                arguments["usage_rights"],
                {
                    "labeled-for-reuse-with-modifications": "sur:fmc",
                    "labeled-for-reuse": "sur:fc",
                    "labeled-for-noncommercial-reuse-with-modification": "sur:fm",
                    "labeled-for-nocommercial-reuse": "sur:f",
                },
            ],
            "size": [
                arguments["size"],
                {
                    "large": "isz:l",
                    "medium": "isz:m",
                    "icon": "isz:i",
                    ">400*300": "isz:lt,islt:qsvga",
                    ">640*480": "isz:lt,islt:vga",
                    ">800*600": "isz:lt,islt:svga",
                    ">1024*768": "visz:lt,islt:xga",
                    ">2MP": "isz:lt,islt:2mp",
                    ">4MP": "isz:lt,islt:4mp",
                    ">6MP": "isz:lt,islt:6mp",
                    ">8MP": "isz:lt,islt:8mp",
                    ">10MP": "isz:lt,islt:10mp",
                    ">12MP": "isz:lt,islt:12mp",
                    ">15MP": "isz:lt,islt:15mp",
                    ">20MP": "isz:lt,islt:20mp",
                    ">40MP": "isz:lt,islt:40mp",
                    ">70MP": "isz:lt,islt:70mp",
                },
            ],
            "type": [
                arguments["type"],
                {
                    "face": "itp:face",
                    "photo": "itp:photo",
                    "clipart": "itp:clipart",
                    "line-drawing": "itp:lineart",
                    "animated": "itp:animated",
                },
            ],
            "time": [
                arguments["time"],
                {
                    "past-24-hours": "qdr:d",
                    "past-7-days": "qdr:w",
                    "past-month": "qdr:m",
                    "past-year": "qdr:y",
                },
            ],
            "aspect_ratio": [
                arguments["aspect_ratio"],
                {
                    "tall": "iar:t",
                    "square": "iar:s",
                    "wide": "iar:w",
                    "panoramic": "iar:xw",
                },
            ],
            "format": [
                arguments["format"],
                {
                    "jpg": "ift:jpg",
                    "gif": "ift:gif",
                    "png": "ift:png",
                    "bmp": "ift:bmp",
                    "svg": "ift:svg",
                    "webp": "webp",
                    "ico": "ift:ico",
                    "raw": "ift:craw",
                },
            ],
        }
        for value in params.values():
            if value[0] is not None:
                ext_param = value[1][value[0]]
                # counter will tell if it is first param added or not
                if counter == 0:
                    # add it to the built url
                    built_url += ext_param
                else:
                    built_url = built_url + "," + ext_param
                counter += 1
        built_url = lang_url + built_url + exact_size + time_range
        return built_url

    # building main search URL

    def build_search_url(
        self, search_term, params, url, similar_images, specific_site, safe_search
    ):
        # check the args and choose the URL
        if url:
            url = url
        elif similar_images:
            keywordem = self.similar_images(similar_images)
            url = (
                "https://www.google.com/search?q="
                + keywordem
                + "&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg"
            )
        elif specific_site:
            url = (
                "https://www.google.com/search?q="
                + quote(search_term.encode("utf-8"))
                + "&as_sitesearch="
                + specific_site
                + "&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch"
                + params
                + "&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg"
            )
        else:
            url = (
                "https://www.google.com/search?q="
                + quote(search_term.encode("utf-8"))
                + "&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch"
                + params
                + "&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg"
            )

        # safe search check
        if safe_search:
            # check safe_search
            safe_search_string = "&safe=active"
            url = url + safe_search_string

        return url

    # measures the file size

    def file_size(self, file_path):
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            size = file_info.st_size
            for x in ["bytes", "KB", "MB", "GB", "TB"]:
                if size < 1024.0:
                    return "%3.1f %s" % (size, x)
                size /= 1024.0
            return size

    # keywords from file
    def keywords_from_file(self, file_name):
        search_keyword = []
        with codecs.open(file_name, "r", encoding="utf-8-sig") as f:
            if ".csv" in file_name or ".txt" in file_name:
                for line in f:
                    if line not in ["\n", "\r\n"]:
                        search_keyword.append(line.replace("\n", "").replace("\r", ""))
            else:
                LOGS.info(
                    "Invalid file type: Valid file types are either .txt or .csv \n"
                    "exiting..."
                )
                sys.exit()
        return search_keyword

    # make directories
    def create_directories(self, main_directory, dir_name, thumbnail, thumbnail_only):
        dir_name_thumbnail = dir_name + " - thumbnail"
        # make a search keyword  directory
        try:
            if not os.path.exists(main_directory):
                os.makedirs(main_directory)
                time.sleep(0.15)
            path = dir_name
            sub_directory = os.path.join(main_directory, path)
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)
            if thumbnail or thumbnail_only:
                sub_directory_thumbnail = os.path.join(
                    main_directory, dir_name_thumbnail
                )
                if not os.path.exists(sub_directory_thumbnail):
                    os.makedirs(sub_directory_thumbnail)
        except OSError as e:
            if e.errno != 17:
                raise

    # Download Image thumbnails

    def download_image_thumbnail(
        self,
        image_url,
        main_directory,
        dir_name,
        return_image_name,
        socket_timeout,
        no_download,
        save_source,
        img_src,
    ):
        if no_download:
            return "success", "Printed url without downloading"
        try:
            req = Request(
                image_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
                },
            )
            try:
                # timeout time to download an image
                timeout = float(socket_timeout) if socket_timeout else 10
                response = urlopen(req, None, timeout)
                data = response.read()
                response.close()

                path = (
                    main_directory
                    + "/"
                    + dir_name
                    + " - thumbnail"
                    + "/"
                    + return_image_name
                )

                try:
                    with open(path, "wb") as output_file:
                        output_file.write(data)
                    if save_source:
                        list_path = main_directory + "/" + save_source + ".txt"
                        with open(list_path, "a") as list_file:
                            list_file.write(path + "\t" + img_src + "\n")
                except OSError as e:
                    download_status = "fail"
                    download_message = (
                        "OSError on an image...trying next one..." + " Error: " + str(e)
                    )
                except IOError as e:
                    download_status = "fail"
                    download_message = (
                        "IOError on an image...trying next one..." + " Error: " + str(e)
                    )

                download_status = "success"
                download_message = (
                    "Completed Image Thumbnail ====> " + return_image_name
                )

            except UnicodeEncodeError as e:
                download_status = "fail"
                download_message = (
                    "UnicodeEncodeError on an image...trying next one..."
                    + " Error: "
                    + str(e)
                )

        except HTTPError as e:  # If there is any HTTPError
            download_status = "fail"
            download_message = (
                "HTTPError on an image...trying next one..." + " Error: " + str(e)
            )

        except URLError as e:
            download_status = "fail"
            download_message = (
                "URLError on an image...trying next one..." + " Error: " + str(e)
            )

        except ssl.CertificateError as e:
            download_status = "fail"
            download_message = (
                "CertificateError on an image...trying next one..."
                + " Error: "
                + str(e)
            )

        except IOError as e:  # If there is any IOError
            download_status = "fail"
            download_message = (
                "IOError on an image...trying next one..." + " Error: " + str(e)
            )
        return download_status, download_message

    # Download Images

    def download_image(
        self,
        image_url,
        image_format,
        main_directory,
        dir_name,
        count,
        socket_timeout,
        prefix,
        no_numbering,
        no_download,
        save_source,
        img_src,
        thumbnail_only,
        format,
        ignore_urls,
    ):
        if ignore_urls and any(url in image_url for url in ignore_urls.split(",")):
            return (
                "fail",
                "Image ignored due to 'ignore url' parameter",
                None,
                image_url,
            )
        if thumbnail_only:
            return (
                "success",
                "Skipping image download...",
                str(image_url[(image_url.rfind("/")) + 1 :]),
                image_url,
            )
        if no_download:
            return "success", "Printed url without downloading", None, image_url
        try:
            req = Request(
                image_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
                },
            )
            try:
                # timeout time to download an image
                timeout = float(socket_timeout) if socket_timeout else 10
                response = urlopen(req, None, timeout)
                data = response.read()
                response.close()

                extensions = [
                    ".jpg",
                    ".jpeg",
                    ".gif",
                    ".png",
                    ".bmp",
                    ".svg",
                    ".webp",
                    ".ico",
                ]
                # keep everything after the last '/'
                image_name = str(image_url[(image_url.rfind("/")) + 1 :])
                if format and (not image_format or image_format != format):
                    download_status = "fail"
                    download_message = "Wrong image format returned. Skipping..."
                    return_image_name = ""
                    absolute_path = ""
                    return (
                        download_status,
                        download_message,
                        return_image_name,
                        absolute_path,
                    )

                if (
                    image_format == ""
                    or not image_format
                    or "." + image_format not in extensions
                ):
                    download_status = "fail"
                    download_message = "Invalid or missing image format. Skipping..."
                    return_image_name = ""
                    absolute_path = ""
                    return (
                        download_status,
                        download_message,
                        return_image_name,
                        absolute_path,
                    )
                if image_name.lower().find("." + image_format) < 0:
                    image_name = image_name + "." + image_format
                else:
                    image_name = image_name[
                        : image_name.lower().find("." + image_format)
                        + (len(image_format) + 1)
                    ]

                # prefix name in image
                prefix = prefix + " " if prefix else ""
                if no_numbering:
                    path = main_directory + "/" + dir_name + "/" + prefix + image_name
                else:
                    path = (
                        main_directory
                        + "/"
                        + dir_name
                        + "/"
                        + prefix
                        + str(count)
                        + "."
                        + image_name
                    )
                try:
                    with open(path, "wb") as output_file:
                        output_file.write(data)
                    if save_source:
                        list_path = main_directory + "/" + save_source + ".txt"
                        with open(list_path, "a") as list_file:
                            list_file.write(path + "\t" + img_src + "\n")
                    absolute_path = os.path.abspath(path)
                except OSError as e:
                    download_status = "fail"
                    download_message = (
                        "OSError on an image...trying next one..." + " Error: " + str(e)
                    )
                    return_image_name = ""
                    absolute_path = ""

                # return image name back to calling method to use it for
                # thumbnail downloads
                download_status = "success"
                download_message = (
                    "Completed Image ====> " + prefix + str(count) + "." + image_name
                )
                return_image_name = prefix + str(count) + "." + image_name

            except UnicodeEncodeError as e:
                download_status = "fail"
                download_message = (
                    "UnicodeEncodeError on an image...trying next one..."
                    + " Error: "
                    + str(e)
                )
                return_image_name = ""
                absolute_path = ""

            except URLError as e:
                download_status = "fail"
                download_message = (
                    "URLError on an image...trying next one..." + " Error: " + str(e)
                )
                return_image_name = ""
                absolute_path = ""

            except BadStatusLine as e:
                download_status = "fail"
                download_message = (
                    "BadStatusLine on an image...trying next one..."
                    + " Error: "
                    + str(e)
                )
                return_image_name = ""
                absolute_path = ""

        except HTTPError as e:  # If there is any HTTPError
            download_status = "fail"
            download_message = (
                "HTTPError on an image...trying next one..." + " Error: " + str(e)
            )
            return_image_name = ""
            absolute_path = ""

        except URLError as e:
            download_status = "fail"
            download_message = (
                "URLError on an image...trying next one..." + " Error: " + str(e)
            )
            return_image_name = ""
            absolute_path = ""

        except ssl.CertificateError as e:
            download_status = "fail"
            download_message = (
                "CertificateError on an image...trying next one..."
                + " Error: "
                + str(e)
            )
            return_image_name = ""
            absolute_path = ""

        except IOError as e:  # If there is any IOError
            download_status = "fail"
            download_message = (
                "IOError on an image...trying next one..." + " Error: " + str(e)
            )
            return_image_name = ""
            absolute_path = ""

        return download_status, download_message, return_image_name, absolute_path

    # Finding 'Next Image' from the given raw page

    def _get_next_item(self, s):
        start_line = s.find("rg_meta notranslate")
        if start_line == -1:  # If no links are found then give an error!
            end_quote = 0
            link = "no_links"
            return link, end_quote
        start_line = s.find('class="rg_meta notranslate">')
        start_object = s.find("{", start_line + 1)
        end_object = s.find("</div>", start_object + 1)
        object_raw = str(s[start_object:end_object])
        # remove escape characters based on python version
        try:
            object_decode = bytes(object_raw, "utf-8").decode("unicode_escape")
            final_object = json.loads(object_decode)
        except BaseException:
            final_object = ""
        return final_object, end_object

    # Getting all links with the help of '_images_get_next_image'

    def _get_image_objects(self, s):
        start_line = s.find("AF_initDataCallback({key: \\'ds:1\\'") - 10
        start_object = s.find("[", start_line + 1)
        end_object = s.find("</script>", start_object + 1) - 4
        object_raw = str(s[start_object:end_object])
        object_decode = bytes(object_raw[:-1], "utf-8").decode("unicode_escape")
        # LOGS.info(_format.paste_text(object_decode[:-15]))
        return json.loads(object_decode[:-15])[31][0][12][2]

    def _get_all_items(self, page, main_directory, dir_name, limit, arguments):
        items = []
        abs_path = []
        errorCount = 0
        i = 0
        count = 1
        # LOGS.info(f"page : {_format.paste_text(page)}")
        image_objects = self._get_image_objects(page)
        while count < limit + 1:
            if not image_objects:
                print("no_links")
                break
            else:
                # format the item for readability
                try:
                    object = self.format_object(image_objects[i])
                    # download the images
                    (
                        download_status,
                        download_message,
                        return_image_name,
                        absolute_path,
                    ) = self.download_image(
                        object["image_link"],
                        object["image_format"],
                        main_directory,
                        dir_name,
                        count,
                        arguments["socket_timeout"],
                        arguments["prefix"],
                        arguments["no_numbering"],
                        arguments["no_download"],
                        arguments["save_source"],
                        object["image_source"],
                        arguments["thumbnail_only"],
                        arguments["format"],
                        arguments["ignore_urls"],
                    )
                except (TypeError, IndexError) as er:
                    LOGS.debug(er)
                    download_status = None

                if download_status == "success":

                    # download image_thumbnails
                    if arguments["thumbnail"] or arguments["thumbnail_only"]:
                        (
                            download_status,
                            download_message_thumbnail,
                        ) = self.download_image_thumbnail(
                            object["image_thumbnail_url"],
                            main_directory,
                            dir_name,
                            return_image_name,
                            arguments["socket_timeout"],
                            arguments["no_download"],
                            arguments["save_source"],
                            object["image_source"],
                            arguments["ignore_urls"],
                        )

                    count += 1
                    object["image_filename"] = return_image_name
                    # Append all the links in the list named 'Links'
                    items.append(object)
                    abs_path.append(absolute_path)
                else:
                    errorCount += 1

                # delay param
                if arguments["delay"]:
                    time.sleep(int(arguments["delay"]))
            i += 1
        if count < limit:
            LOGS.info(
                "\n\nUnfortunately all "
                + str(limit)
                + " could not be downloaded because some images were not downloadable. "
                + str(count - 1)
                + " is all we got for this search filter!"
            )
        return items, errorCount, abs_path

    # Bulk Download

    async def download(self, arguments):
        paths_agg = {}
        # for input coming from other python files
        if __name__ != "__main__":
            # if the calling file contains config_file param
            if "config_file" in arguments:
                records = []
                json_file = json.load(open(arguments["config_file"]))
                for item in json_file["Records"]:
                    arguments = {}
                    for i in args_list:
                        arguments[i] = None
                    for key, value in item.items():
                        arguments[key] = value
                    records.append(arguments)
                total_errors = 0
                for rec in records:
                    paths, errors = await self.download_executor(rec)
                    for i in paths:
                        paths_agg[i] = paths[i]
                    total_errors += errors
                return paths_agg, total_errors
            # if the calling file contains params directly
            paths, errors = await self.download_executor(arguments)
            for i in paths:
                paths_agg[i] = paths[i]
            return paths_agg, errors
        # for input coming from CLI
        paths, errors = await self.download_executor(arguments)
        for i in paths:
            paths_agg[i] = paths[i]
        return paths_agg, errors

    async def download_executor(self, arguments):
        paths = {}
        errorCount = None
        for arg in args_list:
            if arg not in arguments:
                arguments[arg] = None
        # Initialization and Validation of user arguments
        if arguments["keywords"]:
            search_keyword = [str(item) for item in arguments["keywords"].split(",")]

        if arguments["keywords_from_file"]:
            search_keyword = self.keywords_from_file(arguments["keywords_from_file"])

        # both time and time range should not be allowed in the same query
        if arguments["time"] and arguments["time_range"]:
            raise ValueError(
                "Either time or time range should be used in a query. Both cannot be used at the same time."
            )

        # both time and time range should not be allowed in the same query
        if arguments["size"] and arguments["exact_size"]:
            raise ValueError(
                'Either "size" or "exact_size" should be used in a query. Both cannot be used at the same time.'
            )

        # both image directory and no image directory should not be allowed in
        # the same query
        if arguments["image_directory"] and arguments["no_directory"]:
            raise ValueError(
                "You can either specify image directory or specify no image directory, not both!"
            )

        # Additional words added to keywords
        if arguments["suffix_keywords"]:
            suffix_keywords = [
                " " + str(sk) for sk in arguments["suffix_keywords"].split(",")
            ]
        else:
            suffix_keywords = [""]

        # Additional words added to keywords
        if arguments["prefix_keywords"]:
            prefix_keywords = [
                str(sk) + " " for sk in arguments["prefix_keywords"].split(",")
            ]
        else:
            prefix_keywords = [""]

        # Setting limit on number of images to be downloaded
        limit = int(arguments["limit"]) if arguments["limit"] else 100
        if arguments["url"]:
            current_time = str(datetime.datetime.now()).split(".")[0]
            search_keyword = [current_time.replace(":", "_")]

        if arguments["similar_images"]:
            current_time = str(datetime.datetime.now()).split(".")[0]
            search_keyword = [current_time.replace(":", "_")]

        # If single_image or url argument not present then keywords is
        # mandatory argument
        if (
            arguments["single_image"] is None
            and arguments["url"] is None
            and arguments["similar_images"] is None
            and arguments["keywords"] is None
            and arguments["keywords_from_file"] is None
        ):
            LOGS.info(
                "-------------------------------\n"
                "Uh oh! Keywords is a required argument \n\n"
                "Please refer to the documentation on guide to writing queries \n"
                "https://github.com/hardikvasa/google-images-download#examples"
                "\n\nexiting!\n"
                "-------------------------------"
            )
            sys.exit()

        # If this argument is present, set the custom output directory
        main_directory = arguments["output_directory"] or "downloads"
        # Proxy settings
        if arguments["proxy"]:
            os.environ["http_proxy"] = arguments["proxy"]
            os.environ["https_proxy"] = arguments["proxy"]
            # Initialization Complete
        total_errors = 0
        for pky in prefix_keywords:  # 1.for every prefix keywords
            for sky in suffix_keywords:  # 2.for every suffix keywords
                for i in range(len(search_keyword)):  # 3.for every main keyword
                    iteration = (
                        "\n"
                        + "Item no.: "
                        + str(i + 1)
                        + " -->"
                        + " Item name = "
                        + (pky)
                        + (search_keyword[i])
                        + (sky)
                    )
                    search_term = pky + search_keyword[i] + sky

                    if arguments["image_directory"]:
                        dir_name = arguments["image_directory"]
                    elif arguments["no_directory"]:
                        dir_name = ""
                    else:
                        dir_name = search_term + (
                            "-" + arguments["color"] if arguments["color"] else ""
                        )  # sub-directory

                    if not arguments["no_download"]:
                        self.create_directories(
                            main_directory,
                            dir_name,
                            arguments["thumbnail"],
                            arguments["thumbnail_only"],
                        )  # create directories in OS

                    params = self.build_url_parameters(
                        arguments
                    )  # building URL with params

                    url = self.build_search_url(
                        search_term,
                        params,
                        arguments["url"],
                        arguments["similar_images"],
                        arguments["specific_site"],
                        arguments["safe_search"],
                    )  # building main search url

                    if limit < 101:
                        # download page
                        raw_html = await self.download_page(url)
                    else:
                        raw_html = self.download_extended_page(
                            url, arguments["chromedriver"]
                        )

                    items, errorCount, abs_path = self._get_all_items(
                        raw_html, main_directory, dir_name, limit, arguments
                    )  # get all image items and download images
                    paths[pky + search_keyword[i] + sky] = abs_path

                    # dumps into a json file
                    if arguments["extract_metadata"]:
                        try:
                            if not os.path.exists("logs"):
                                os.makedirs("logs")
                        except OSError as e:
                            LOGS.exception(e)
                        with open(
                            "logs/" + search_keyword[i] + ".json", "w"
                        ) as json_file:
                            json.dump(items, json_file, indent=4, sort_keys=True)
                    # Related images
                    if arguments["related_images"]:
                        tabs = self.get_all_tabs(raw_html)
                        for key, value in tabs.items():
                            final_search_term = search_term + " - " + key
                            if limit < 101:
                                new_raw_html = await self.download_page(
                                    value
                                )  # download page
                            else:
                                new_raw_html = self.download_extended_page(
                                    value, arguments["chromedriver"]
                                )
                            self.create_directories(
                                main_directory,
                                final_search_term,
                                arguments["thumbnail"],
                                arguments["thumbnail_only"],
                            )
                            self._get_all_items(
                                new_raw_html,
                                main_directory,
                                search_term + " - " + key,
                                limit,
                                arguments,
                            )

                    total_errors += errorCount
        return paths, total_errors
