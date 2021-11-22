from typing import Dict, List, Any

import youtubesearchpython as ysp

from pyou.temp_file_handler import TempFileHandler


class YoutubeSearch:
    def __init__(self) -> None:
        self.temp_file_handler = TempFileHandler()

    def search(self, query: str) -> List[Dict[str, Any]]:
        search_result = ysp.VideosSearch(query)
        result = search_result.result()["result"]

        return [self._filter_results(item) for item in result]

    def _filter_results(self, result: Dict[str, Any]) -> Dict[str, Any]:
        accepted_keys = [
            "title",
            "publishedTime",
            "duration",
            "viewCount",
            "thumbnails",
            "richThumbnail",
            "channel",
            "link"
        ]

        temp_dict = {}

        for item in result:
            if item not in accepted_keys:
                continue

            # A value of None for either publishedTime or viewCount means that the video
            # will premiere or has not been released yet for viewing
            if item == "publishedTime":
                temp_dict[item] = result[item] if result[item] else "Will Premiere"
            elif item == "viewCount":
                temp_dict[item] = result[item] if result[item]["short"] else {"short": "No views"}
            elif item == "thumbnails":
                temp_dict["thumbnail"] = self.temp_file_handler.add_file(result[item][0]["url"])
            elif item == "richThumbnail":
                temp_dict[item] = result[item]["url"] if result[item] else None
            else:
                temp_dict[item] = result[item]

        return temp_dict
