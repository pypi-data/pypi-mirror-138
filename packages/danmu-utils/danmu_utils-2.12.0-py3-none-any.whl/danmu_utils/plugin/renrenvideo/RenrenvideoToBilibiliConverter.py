import json
from danmu_utils.common.IConverter import IConverter
from danmu_utils.plugin.bilibili.BilibiliGenerator import  BilibiliGenerator


class RenrenvideoToBilibiliConverter(IConverter):
    @property
    def DANMU_TYPE_SRC(self):
        return 'renrenvideo'

    @property
    def DANMU_TYPE_DST(self):
        return 'bilibili'

    @property
    def DANMU_EXTNAME_SRC(self):
        return 'renrenvideojson'

    @property
    def DANMU_EXTNAME_DST(self):
        return 'xml'

    def convert(self, data):
        bilibiliGenerator = BilibiliGenerator()
        try:
            item_src = json.loads(data)
        except Exception as e:
            print(e)
            return None
        list_src = None
        if isinstance(item_src, list):
            list_src = item_src
        else:
            list_src = item_src['data']['danmuList']
        for entry_src in list_src:
            try:
                text = entry_src['d']
                p_list = entry_src['p'].split(sep=',')
                send_time = float(p_list[0])
                size = int(p_list[2])
                color = int(p_list[3])
            except Exception as e:
                print(e)
                continue
            bilibiliGenerator.append(text, send_time, size=size, color=color)
        return bilibiliGenerator.output()


from danmu_utils.common.plugin_collection import add_convert_tool

add_convert_tool(RenrenvideoToBilibiliConverter().DANMU_TYPE_SRC, RenrenvideoToBilibiliConverter().DANMU_TYPE_DST, RenrenvideoToBilibiliConverter)
