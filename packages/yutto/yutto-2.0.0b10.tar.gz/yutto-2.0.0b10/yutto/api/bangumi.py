import re
from typing import Any, Optional, TypedDict

from aiohttp import ClientSession

from yutto.exceptions import NoAccessPermissionError, UnSupportedTypeError
from yutto.bilibili_typing.codec import audio_codec_map, video_codec_map
from yutto._typing import AudioUrlMeta, AvId, BvId, CId, EpisodeId, MediaId, MultiLangSubtitle, SeasonId, VideoUrlMeta
from yutto.utils.console.logger import Logger
from yutto.utils.fetcher import Fetcher
from yutto.utils.metadata import MetaData
from yutto.utils.time import get_time_str_by_now, get_time_str_by_stamp


class BangumiListItem(TypedDict):
    id: int
    name: str
    cid: CId
    episode_id: EpisodeId
    avid: AvId
    is_section: bool  # 是否属于专区
    metadata: Optional[MetaData]


async def get_season_id_by_media_id(session: ClientSession, media_id: MediaId) -> SeasonId:
    home_url = "https://www.bilibili.com/bangumi/media/md{media_id}".format(media_id=media_id)
    season_id = SeasonId("")
    regex_season_id = re.compile(r'"param":{"season_id":(\d+),"season_type":\d+}')
    if match_obj := regex_season_id.search(await Fetcher.fetch_text(session, home_url)):
        season_id = match_obj.group(1)
    return SeasonId(str(season_id))


async def get_season_id_by_episode_id(session: ClientSession, episode_id: EpisodeId) -> SeasonId:
    home_url = "https://www.bilibili.com/bangumi/play/ep{episode_id}".format(episode_id=episode_id)
    season_id = SeasonId("")
    regex_season_id = re.compile(r'"id":\d+,"ssId":(\d+)')
    if match_obj := regex_season_id.search(await Fetcher.fetch_text(session, home_url)):
        season_id = match_obj.group(1)
    return SeasonId(str(season_id))


async def get_bangumi_title(session: ClientSession, season_id: SeasonId) -> str:
    play_url = "https://api.bilibili.com/pgc/view/web/season?season_id={season_id}".format(season_id=season_id)
    resp = await Fetcher.fetch_json(session, play_url)
    title = resp["result"]["title"]
    return title


async def get_bangumi_title_from_html(session: ClientSession, season_id: SeasonId) -> str:
    """原来用的从 HTML 里解析标题，但由于 HTML 经常改版，所以暂时弃用，未来可能删掉"""
    play_url = "https://www.bilibili.com/bangumi/play/ss{season_id}".format(season_id=season_id)
    regex_title = re.compile(r'<a href=".+" target="_blank" title="(.*?)" class="media-title">(?P<title>.*?)</a>')
    if match_obj := regex_title.search(await Fetcher.fetch_text(session, play_url)):
        title = match_obj.group("title")
    else:
        title = "呐，我也不知道是什么标题呢～"
    return title


async def get_bangumi_list(
    session: ClientSession, season_id: SeasonId, with_metadata: bool = False
) -> list[BangumiListItem]:
    list_api = "http://api.bilibili.com/pgc/view/web/season?season_id={season_id}"
    resp_json = await Fetcher.fetch_json(session, list_api.format(season_id=season_id))
    result = resp_json["result"]
    section_episodes = []
    for section in result.get("section", []):
        section_episodes += section["episodes"]
    return [
        {
            "id": i + 1,
            "name": _bangumi_episode_title(item["title"], item["long_title"]),
            "cid": CId(str(item["cid"])),
            "episode_id": EpisodeId(str(item["id"])),
            "avid": BvId(item["bvid"]),
            "is_section": i >= len(result["episodes"]),
            "metadata": _parse_bangumi_metadata(item) if with_metadata else None,
        }
        for i, item in enumerate(result["episodes"] + section_episodes)
    ]


async def get_bangumi_playurl(
    session: ClientSession, avid: AvId, episode_id: EpisodeId, cid: CId
) -> tuple[list[VideoUrlMeta], list[AudioUrlMeta]]:
    play_api = "https://api.bilibili.com/pgc/player/web/playurl?avid={aid}&bvid={bvid}&ep_id={episode_id}&cid={cid}&qn=127&fnver=0&fnval=16&fourk=1"

    async with session.get(
        play_api.format(**avid.to_dict(), cid=cid, episode_id=episode_id), proxy=Fetcher.proxy
    ) as resp:
        if not resp.ok:
            raise NoAccessPermissionError("无法下载该视频（cid: {cid}）".format(cid=cid))
        resp_json = await resp.json()
        if resp_json.get("result") is None:
            raise NoAccessPermissionError("无法下载该视频（cid: {cid}），原因：{msg}".format(cid=cid, msg=resp_json.get("message")))
        if resp_json["result"].get("dash") is None:
            raise UnSupportedTypeError("该视频（cid: {cid}）尚不支持 DASH 格式".format(cid=cid))
        if resp_json["result"]["is_preview"] == 1:
            Logger.warning("视频（cid: {cid}）是预览视频".format(cid=cid))
        return (
            [
                {
                    "url": video["base_url"],
                    "mirrors": video["backup_url"] if video["backup_url"] is not None else [],
                    "codec": video_codec_map[video["codecid"]],
                    "width": video["width"],
                    "height": video["height"],
                    "quality": video["id"],
                }
                for video in resp_json["result"]["dash"]["video"]
            ],
            [
                {
                    "url": audio["base_url"],
                    "mirrors": audio["backup_url"] if audio["backup_url"] is not None else [],
                    "codec": audio_codec_map[audio["codecid"]],
                    "width": 0,
                    "height": 0,
                    "quality": audio["id"],
                }
                for audio in resp_json["result"]["dash"]["audio"]
            ],
        )


async def get_bangumi_subtitles(session: ClientSession, avid: AvId, cid: CId) -> list[MultiLangSubtitle]:
    subtitile_api = "https://api.bilibili.com/x/player/v2?cid={cid}&aid={aid}&bvid={bvid}"
    subtitile_url = subtitile_api.format(**avid.to_dict(), cid=cid)
    subtitles_info = (await Fetcher.fetch_json(session, subtitile_url))["data"]["subtitle"]
    return [
        {
            "lang": sub_info["lan_doc"],
            "lines": (await Fetcher.fetch_json(session, "https:" + sub_info["subtitle_url"]))["body"],
        }
        for sub_info in subtitles_info["subtitles"]
    ]


def _bangumi_episode_title(title: str, extra_title: str) -> str:
    title_parts: list[str] = []
    if re.match(r"^\d*\.?\d*$", title):
        title_parts.append(f"第{title}话")
    else:
        title_parts.append(title)

    if extra_title:
        title_parts.append(extra_title)

    return " ".join(title_parts)


def _parse_bangumi_metadata(item: dict[str, Any]) -> MetaData:

    return MetaData(
        title=_bangumi_episode_title(item["title"], item["long_title"]),
        show_title=item["share_copy"],
        plot=item["share_copy"],
        thumb=item["cover"],
        premiered=get_time_str_by_stamp(item["pub_time"]),
        dataadded=get_time_str_by_now(),
        source="",  # TODO
        original_filename="",  # TODO
    )
