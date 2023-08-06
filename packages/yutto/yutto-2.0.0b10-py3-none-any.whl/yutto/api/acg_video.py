import json
import re
from typing import Optional, TypedDict

from aiohttp import ClientSession

from yutto.api.info import get_video_info
from yutto.exceptions import NoAccessPermissionError, UnSupportedTypeError
from yutto.bilibili_typing.codec import audio_codec_map, video_codec_map
from yutto._typing import AudioUrlMeta, AvId, CId, MultiLangSubtitle, VideoUrlMeta
from yutto.utils.console.logger import Logger
from yutto.utils.fetcher import Fetcher
from yutto.utils.metadata import MetaData
from yutto.utils.time import get_time_str_by_now, get_time_str_by_stamp


class AcgVideoListItem(TypedDict):
    id: int
    name: str
    avid: AvId
    cid: CId
    metadata: Optional[MetaData]


async def get_acg_video_title(session: ClientSession, avid: AvId) -> str:
    return (await get_video_info(session, avid))["title"]


async def get_acg_video_pubdate(session: ClientSession, avid: AvId) -> str:
    return (await get_video_info(session, avid))["pubdate"]


async def get_acg_video_list(session: ClientSession, avid: AvId, with_metadata: bool = False) -> list[AcgVideoListItem]:
    list_api = "https://api.bilibili.com/x/player/pagelist?aid={aid}&bvid={bvid}&jsonp=jsonp"
    res_json = await Fetcher.fetch_json(session, list_api.format(**avid.to_dict()))
    if res_json.get("data") is None:
        Logger.warning(f"啊叻？视频 {avid} 不见了诶")
        return []
    acg_video_info: list[AcgVideoListItem] = [
        {
            "id": i + 1,
            "name": item["part"],
            "avid": avid,
            "cid": CId(str(item["cid"])),
            "metadata": None,
        }
        for i, item in enumerate(res_json["data"])
    ]

    if with_metadata:
        metadata_list = await get_acg_video_metadata(session, avid)
        assert len(metadata_list) == len(acg_video_info)
        for info, metadata in zip(acg_video_info, metadata_list):
            info["metadata"] = metadata
    return acg_video_info


async def get_acg_video_playurl(
    session: ClientSession, avid: AvId, cid: CId
) -> tuple[list[VideoUrlMeta], list[AudioUrlMeta]]:
    # 4048 = 16(useDash) | 64(useHDR) | 128(use4K) | 256(useDolby) | 512(useXXX) | 1024(use8K) | 2048(useAV1)
    play_api = "https://api.bilibili.com/x/player/playurl?avid={aid}&bvid={bvid}&cid={cid}&qn=127&type=&otype=json&fnver=0&fnval=4048&fourk=1"

    async with session.get(play_api.format(**avid.to_dict(), cid=cid), proxy=Fetcher.proxy) as resp:
        if not resp.ok:
            raise NoAccessPermissionError(f"无法下载该视频（cid: {cid}）")
        resp_json = await resp.json()
        if resp_json.get("data") is None:
            raise NoAccessPermissionError(f"无法下载该视频（cid: {cid}），原因：{resp_json.get('message')}")
        if resp_json["data"].get("dash") is None:
            raise UnSupportedTypeError(f"该视频（cid: {cid}）尚不支持 DASH 格式")
        # TODO: 处理 resp_json["data"]["dash"]["dolby"]，应当是 Dolby 的音频流
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
                for video in resp_json["data"]["dash"]["video"]
            ]
            if resp_json["data"]["dash"]["video"]
            else [],
            [
                {
                    "url": audio["base_url"],
                    "mirrors": audio["backup_url"] if audio["backup_url"] is not None else [],
                    "codec": audio_codec_map[audio["codecid"]],
                    "width": 0,
                    "height": 0,
                    "quality": audio["id"],
                }
                for audio in resp_json["data"]["dash"]["audio"]
            ]
            if resp_json["data"]["dash"]["audio"]
            else [],
        )


async def get_acg_video_subtitles(session: ClientSession, avid: AvId, cid: CId) -> list[MultiLangSubtitle]:
    subtitile_api = "https://api.bilibili.com/x/player.so?aid={aid}&bvid={bvid}&id=cid:{cid}"
    subtitile_url = subtitile_api.format(**avid.to_dict(), cid=cid)
    res_text = await Fetcher.fetch_text(session, subtitile_url)
    if subtitle_json_text_match := re.search(r"<subtitle>(.+)</subtitle>", res_text):
        subtitle_json = json.loads(subtitle_json_text_match.group(1))
        return [
            {
                "lang": sub_info["lan_doc"],
                "lines": (await Fetcher.fetch_json(session, "https:" + sub_info["subtitle_url"]))["body"],
            }
            for sub_info in subtitle_json["subtitles"]
        ]
    else:
        return []


async def get_acg_video_metadata(session: ClientSession, avid: AvId) -> list[MetaData]:
    web_interface_api = "https://api.bilibili.com/x/web-interface/view?aid={aid}&bvid={bvid}"
    web_interface_url = web_interface_api.format(**avid.to_dict())
    res_json = await Fetcher.fetch_json(session, web_interface_url)
    return [
        MetaData(
            title=page_info["part"],
            show_title=page_info["part"],
            plot=res_json["data"]["desc"],
            thumb=page_info["first_frame"] if page_info.get("first_frame") else res_json["data"]["pic"],
            premiered=get_time_str_by_stamp(res_json["data"]["pubdate"]),
            dataadded=get_time_str_by_now(),
            source="",  # TODO
            original_filename="",  # TODO
        )
        for page_info in res_json["data"]["pages"]
    ]
