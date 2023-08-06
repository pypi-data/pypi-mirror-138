from typing import NamedTuple, Optional, TypedDict

from yutto.bilibili_typing.codec import AudioCodec, VideoCodec
from yutto.bilibili_typing.quality import AudioQuality, VideoQuality
from yutto.utils.danmaku import DanmakuData
from yutto.utils.metadata import MetaData
from yutto.utils.subtitle import SubtitleData


class BilibiliId(NamedTuple):
    value: str

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: "BilibiliId") -> bool:
        return self.value == other.value


class AvId(BilibiliId):
    """AID 与 BVID 的统一，大多数 API 只需要其中一种即可正常工作"""

    def to_dict(self) -> dict[str, str]:
        raise NotImplementedError("请不要直接使用 AvId")

    def to_url(self) -> str:
        raise NotImplementedError("请不要直接使用 AvId")


class AId(AvId):
    """AID"""

    def to_dict(self):
        return {"aid": self.value, "bvid": ""}

    def to_url(self) -> str:
        return f"https://www.bilibili.com/video/av{self.value}"


class BvId(AvId):
    """BVID"""

    def to_dict(self):
        return {
            "aid": "",
            "bvid": self.value,
        }

    def to_url(self) -> str:
        return f"https://www.bilibili.com/video/{self.value}"


class CId(BilibiliId):
    """视频 ID"""

    def to_dict(self):
        return {"cid": self.value}


class EpisodeId(BilibiliId):
    """番剧剧集 ID"""

    def to_dict(self):
        return {"episode_id": self.value}


class MediaId(BilibiliId):
    """番剧 ID"""

    def to_dict(self):
        return {"media_id": self.value}


class SeasonId(BilibiliId):
    """番剧（季） ID"""

    def to_dict(self):
        return {"season_id": self.value}


class MId(BilibiliId):
    """用户 ID"""

    def to_dict(self):
        return {"mid": self.value}


class FId(BilibiliId):
    """收藏夹 ID"""

    def to_dict(self):
        return {"fid": self.value}


class SeriesId(BilibiliId):
    """视频合集 ID"""

    def to_dict(self):
        return {"series_id": self.value}


class VideoUrlMeta(TypedDict):
    url: str
    mirrors: list[str]
    codec: VideoCodec
    width: int
    height: int
    quality: VideoQuality


class AudioUrlMeta(TypedDict):
    url: str
    mirrors: list[str]
    codec: AudioCodec
    width: int
    height: int
    quality: AudioQuality


class MultiLangSubtitle(TypedDict):
    lang: str
    lines: SubtitleData


class EpisodeData(TypedDict):
    videos: list[VideoUrlMeta]
    audios: list[AudioUrlMeta]
    subtitles: list[MultiLangSubtitle]
    metadata: Optional[MetaData]
    danmaku: DanmakuData
    output_dir: str
    tmp_dir: str
    filename: str


class DownloaderOptions(TypedDict):
    require_video: bool
    video_quality: VideoQuality
    video_download_codec: VideoCodec
    video_save_codec: str
    require_audio: bool
    audio_quality: AudioQuality
    audio_download_codec: AudioCodec
    audio_save_codec: str
    overwrite: bool
    block_size: int
    num_workers: int


class FavouriteMetaData(TypedDict):
    fid: FId
    title: str


if __name__ == "__main__":
    aid = AId("add")
    cid = CId("xxx")
    print("?aid={aid}&bvid={bvid}&cid={cid}".format(**aid.to_dict(), **cid.to_dict()))
