import urllib.request

from danmu_utils.common.IDownloader import IDownloader
import danmu_utils.plugin.bilibili2.dm_pb2 as Danmaku


class Bilibili2Downloader(IDownloader):
    @property
    def DANMU_TYPE(self):
        return 'bilibili2'

    @property
    def DANMU_EXTNAME(self):
        return 'bilibili2'

    @property
    def DANMU_LIST_EXTNAME(self):
        return 'bilibili2list'

    def _download(self, cid, pid):
        segment_index = 1
        total_danmaku_seg = None
        while (True):
            url = 'https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid=%s&pid=%s&segment_index=%s' % (cid, pid, segment_index)
            try:
                with urllib.request.urlopen(url) as f:
                    danmu = f.read()
            except urllib.error.HTTPError as err:
                if err.code == 304:
                    break
                else:
                    raise err
            danmaku_seg = Danmaku.DmSegMobileReply()
            danmaku_seg.ParseFromString(danmu)
            if total_danmaku_seg == None:
                total_danmaku_seg = danmaku_seg
            else:
                total_danmaku_seg.elems.extend(danmaku_seg.elems)
            segment_index = segment_index + 1
        return total_danmaku_seg.SerializeToString()

    def download(self, line):
        line_res = []
        line_params = line.strip('\n').split('\t')
        cid = line_params[0]
        pid = line_params[1]
        filename = line_params[2]
        res = self._download(cid=cid, pid=pid)
        item_res = {}
        item_res['filename'] = filename + '.' + self.DANMU_EXTNAME
        item_res['data'] = res
        line_res.append(item_res)
        return line_res


from danmu_utils.common.plugin_collection import add_download_tool
add_download_tool(Bilibili2Downloader().DANMU_TYPE, Bilibili2Downloader)
