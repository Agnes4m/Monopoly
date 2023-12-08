import json
from typing import Dict, List, Union

import aiofiles
from gsuid_core.bot import Bot
from gsuid_core.message_models import Button
from gsuid_core.models import Event
from gsuid_core.sv import SV
from gsuid_core.utils.image.image_tools import get_event_avatar

# from ..utils.load_data import load_mono
# from ..utils.resource_path import all_mono, history_path

sv_mono_help = SV('大富翁帮助')
sv_mono_start = SV('大富翁开始游戏')
sv_mono_hot = SV('结束游戏')


@sv_mono_help.on_command(('大富翁帮助', "mono帮助"))
async def send_help(bot: Bot, ev: Event):
    await bot.send_option(
        '欢迎游玩大富翁游戏!',
        [''],
        True,
    )


@sv_mono_start.on_command(('大富翁开始', "mono开始"))
async def send_mono(bot: Bot, ev: Event):
    usr_id = ev.user_id
    usr_image = get_event_avatar(ev)

    mono = await load_mono(mono_name)
    if mono is None:
        return await bot.send_option(
            '该测试不存在噢！请输入正确的测试名称！或者查看帮助以获得更多信息！',
            ['热门测试', '全部测试列表', '心理测试帮助'],
            True,
        )

    if 'start' in mono.questions:
        start = mono.questions['start']
    elif '1' in mono.questions:
        start = mono.questions['1']
    else:
        return await bot.send_option(
            '该测试不存在噢！请输入正确的测试名称！或者查看帮助以获得更多信息！',
            ['热门测试', '全部测试列表', '心理测试帮助'],
            True,
        )

    _path = []
    _answer = None
    _point = 0
    _key = []

    # 开始测试
    while True:
        resp = await bot.receive_resp(
            start.question, [a for a in start.answer], True
        )
        if resp is not None:
            user_answer = resp.text.strip()
            if user_answer not in start.answer:
                await bot.send('你的回答不在选项中噢...请重新回答!')
                continue
            _to = start.answer[user_answer].to
            if _to == 'end':
                _answer = _to
                break
            elif _to[0] == 'A' or _to[0] == 'a':
                _answer = _to[1:]
                break
            _point += start.answer[user_answer].point
            _key.extend(start.answer[user_answer].key)
            _path.append(user_answer)
            start = mono.questions[_to]
        else:
            break

    if _answer is None:
        return await bot.send('回答问题超时噢, 可以重新开始测试~, @我并发送 心理测试帮助 可以获得更多信息！')

    result = None
    _title = None

    # 结束
    if _answer == 'end':
        for _num in mono.results:
            _title = _num
            result = mono.results[_num]
            if _point >= result.point_down and _point <= result.point_up:
                _need_key = set(result.need_key)
                _self_key = set(_key)
                if _need_key.issubset(_self_key):
                    await bot.send_option(
                        result.detail, ['热门测试', '全部测试列表', '心理测试帮助'], True
                    )
    else:
        for _num in mono.results:
            if _num == _answer:
                _title = _num
                result = mono.results[_num]
                await bot.send_option(
                    result.detail, ['热门测试', '全部测试列表', '心理测试帮助'], True
                )

    if result is not None:
        # 保存每个人的结果
        _record = {
            'bot_id': ev.real_bot_id,
            'group': ev.group_id,
            'user': ev.user_id,
            'path': _path,
            'point': _point,
            'key': _key,
            'answer': _answer,
            'result': _title,
        }

        path = history_path / f'{mono_name}.json'
        if not path.exists():
            record = [_record]
            async with aiofiles.open(path, 'x', encoding='UTF-8') as f:
                await f.write(json.dumps(record, ensure_ascii=False, indent=4))
        else:
            async with aiofiles.open(path, 'x', encoding='UTF-8') as f:
                record: List[Dict] = json.loads(await f.read())
                record.append(_record)
                await f.write(json.dumps(record, ensure_ascii=False, indent=4))
