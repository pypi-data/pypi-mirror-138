import json
from danmu_utils.common.IConverter import IConverter
from danmu_utils.plugin.bilibili.BilibiliGenerator import  BilibiliGenerator
import danmu_utils.plugin.bilibili2.dm_pb2 as Danmaku


class Bilibili2ToBilibiliConverter(IConverter):
    @property
    def DANMU_TYPE_SRC(self):
        return 'bilibili2'

    @property
    def DANMU_TYPE_DST(self):
        return 'bilibili'

    @property
    def DANMU_EXTNAME_SRC(self):
        return 'bilibili2'

    @property
    def DANMU_EXTNAME_DST(self):
        return 'xml'

    @property
    def READ_FILE_AS_BYTE(self):
        return True

    def convert(self, data):
        bilibiliGenerator = BilibiliGenerator()
        try:
            danmaku_seg = Danmaku.DmSegMobileReply()
            danmaku_seg.ParseFromString(data)
        except Exception as e:
            print(e)
            return None
        list_src = danmaku_seg.elems
        for entry_src in list_src:
            try:
                text = entry_src.content
                send_time = float(entry_src.progress) / 1000
                size = int(entry_src.fontsize)
                color = int(entry_src.color)
            except Exception as e:
                print(e)
                continue
            bilibiliGenerator.append(text, send_time, size=size, color=color)
        return bilibiliGenerator.output()


from danmu_utils.common.plugin_collection import add_convert_tool

add_convert_tool(Bilibili2ToBilibiliConverter().DANMU_TYPE_SRC, Bilibili2ToBilibiliConverter().DANMU_TYPE_DST, Bilibili2ToBilibiliConverter)
