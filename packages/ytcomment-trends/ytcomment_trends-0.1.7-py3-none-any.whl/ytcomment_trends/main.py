from .controllers.google_api import GoogleAPIAuth, get_comments
from .controllers.nlp import OsetiAnalyzer

from typing import List, Dict

import pandas as pd
import datetime

class CommentAnalyzer:
    """YouTube comment analyzer
    Args:
        video_id (str): YouTube video ID of the video to get comments from
        api_key (str): YouTube API key (make sure to enable YouTube Data API V3)
    """

    def __init__(self, video_id: str, api_key: str, next_page_token: str=None):
        self.video_id = video_id
        self.api_token_obj = GoogleAPIAuth(api_key).get_authenticated_service()
        self.next_page_token = next_page_token

    def get_comments(self) -> tuple[List[Dict], str]:
        """get comments from video

        Returns:
            List[Dict]: comments
        """
        return get_comments(self.api_token_obj, self.video_id, next_page_token=self.next_page_token)

    def get_analyzed_comments(self, comments: List[Dict]) -> List[Dict]:
        """add oseti score

        Args:
            comments (List[Dict]): comments in list-in-dict format

        Returns:
            List[Dict]: comments with oseti score
        """
        oa = OsetiAnalyzer()
        for comment in comments:
            try:
                comment["oseti_score"] = oa.analyze(comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
            except:
                comment["oseti_score"] = 0
        return comments

    def get_summarized_comments(self, comments: List[Dict], summarized_in: str = "W") -> Dict:
        """get summarized comments grouped by datetime (default week)

        Args:
            comments (List[Dict]): comments
            summarized_in (str, optional): how to group by comments. Please refer to pandas resample documentation. Defaults to "W".

        Returns:
            pd.DataFrame: summarized comments grouped by datetime (default week)
        """
        df = pd.json_normalize(comments)
        df['snippet.topLevelComment.snippet.publishedAt'] = pd.to_datetime(df['snippet.topLevelComment.snippet.publishedAt'])
        df = df.set_index('snippet.topLevelComment.snippet.publishedAt')
        ca_summarized = df.resample(summarized_in, label="left").sum()
        dts = [dt.astype('datetime64[D]').astype(datetime.datetime) for dt in list(ca_summarized.index.values)]
        oseti_scores = []
        for s, n in zip(list(ca_summarized['oseti_score']), list(ca_summarized['snippet.isPublic'])):
            if n > 0:
                oseti_scores.append(s / n)
            else:
                oseti_scores.append(0)
        return {k: {"oseti_score": v, "comments": c} for k, v, c in zip(dts, oseti_scores, ca_summarized['snippet.isPublic'])}