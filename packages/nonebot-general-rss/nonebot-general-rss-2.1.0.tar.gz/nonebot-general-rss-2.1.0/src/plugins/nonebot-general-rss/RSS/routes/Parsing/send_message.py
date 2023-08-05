import nonebot
from nonebot import logger
from nonebot.adapters.onebot.v11 import NetworkError

from ....bot_info import (get_bot_friend_list, get_bot_group_list,
                          get_bot_guild_channel_list)
from ....RSS import rss_class


# 发送消息
async def send_msg(rss: rss_class.Rss, msg: str, item: dict) -> bool:
    bot = nonebot.get_bot()
    flag = False
    if not msg:
        return False
    if rss.user_id:
        friend_list = await get_bot_friend_list(bot)
        for user_id in rss.user_id:
            if int(user_id) not in friend_list:
                logger.error(
                    f"QQ号[{user_id}]不是Bot[{bot.self_id}]的好友 链接：[{item['link']}]"
                )
                continue
            try:
                await bot.send_private_msg(user_id=int(user_id), message=str(msg))
                flag = True
            except NetworkError:
                if item.get("count") == 3:
                    logger.error(f"网络错误，消息发送失败，已达最大重试次数！链接：[{item['link']}]")
                else:
                    logger.warning(f"网络错误，消息发送失败，将重试")
            except Exception as e:
                logger.error(f"E1: {e} 链接：[{item['link']}]")

    if rss.group_id:
        group_list = await get_bot_group_list(bot)
        for group_id in rss.group_id:
            if int(group_id) not in group_list:
                logger.error(f"Bot[{bot.self_id}]未加入群组[{group_id}] 链接：[{item['link']}]")
                continue
            try:
                await bot.send_group_msg(group_id=int(group_id), message=str(msg))
                flag = True
            except NetworkError:
                if item.get("count") == 3:
                    logger.error(f"网络错误，消息发送失败，已达最大重试次数！链接：[{item['link']}]")
                else:
                    logger.warning(f"网络错误，消息发送失败，将重试")
            except Exception as e:
                logger.error(f"E2: {e} 链接：[{item['link']}]")

    if rss.guild_channel_id:
        for guild_channel_id in rss.guild_channel_id:
            id = guild_channel_id.split("@")
            guild_id = str(id[0])
            channel_id = str(id[1])

            guild_channel_list = await get_bot_guild_channel_list(
                bot, guild_id=guild_id
            )

            if channel_id not in guild_channel_list:
                logger.error(
                    f"Bot[{bot.self_id}]未加入频道[{guild_id}]的子频道[{channel_id}] 链接：[{item['link']}]"
                )
                continue
            try:
                await bot.send_guild_channel_msg(
                    message=str(msg), guild_id=guild_id, channel_id=channel_id
                )
                flag = True
            except NetworkError:
                if item.get("count") == 3:
                    logger.error(f"网络错误，消息发送失败，已达最大重试次数！链接：[{item['link']}]")
                else:
                    logger.warning(f"网络错误，消息发送失败，将重试")
            except Exception as e:
                logger.error(f"E3: {e} 链接：[{item['link']}]")
    return flag
