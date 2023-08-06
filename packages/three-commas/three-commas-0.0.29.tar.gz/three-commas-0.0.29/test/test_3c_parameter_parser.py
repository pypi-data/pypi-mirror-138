from src.three_commas.model import Bot
import json
import datetime


def test_fields_are_parsed():
    with open('test/sample_data/bots/usdt/bot_show_with_events_usdt.json') as f:
        bot_show: Bot = Bot.of(json.loads(f.read()))
        assert bot_show.get_base_order_volume() == 10.0
        assert bot_show.get_base_order_volume(parsed=False) == "10.0"

        bot_show.set_base_order_volume(None)
        assert bot_show.get_base_order_volume() is None
        assert bot_show.get_base_order_volume(parsed=False) is None

        del bot_show['base_order_volume']
        assert bot_show.get_base_order_volume() is None
        assert bot_show.get_base_order_volume(parsed=False) is None


def test_ts_are_parsed():
    with open('test/sample_data/bots/usdt/bot_show_with_events_usdt.json') as f:
        bot_show: Bot = Bot.of(json.loads(f.read()))
        assert isinstance(bot_show.get_created_at(), str)
        assert isinstance(bot_show.get_created_at(parsed=True), datetime.datetime)
