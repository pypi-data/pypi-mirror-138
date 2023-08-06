import json
from danmu_utils.common.IConverter import IConverter
from danmu_utils.plugin.bilibili.BilibiliGenerator import  BilibiliGenerator


class VqqToBilibiliConverter(IConverter):
    @property
    def DANMU_TYPE_SRC(self):
        return 'vqq'

    @property
    def DANMU_TYPE_DST(self):
        return 'bilibili'

    @property
    def DANMU_EXTNAME_SRC(self):
        return 'vqqjson'

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
        for entry_src in item_src['comments']:
            try:
                text = entry_src['content']
                send_time = float(entry_src['timepoint'])
            except Exception as e:
                print(e)
                continue
            bilibiliGenerator.append(text, send_time)
        return bilibiliGenerator.output()


from danmu_utils.common.plugin_collection import add_convert_tool

add_convert_tool(VqqToBilibiliConverter().DANMU_TYPE_SRC, VqqToBilibiliConverter().DANMU_TYPE_DST, VqqToBilibiliConverter)
