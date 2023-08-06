import urllib.request
import json


from danmu_utils.common.IDownloader import IDownloader


class VqqDownloader(IDownloader):
    @property
    def DANMU_TYPE(self):
        return 'vqq'

    @property
    def DANMU_EXTNAME(self):
        return 'vqqjson'

    @property
    def DANMU_LIST_EXTNAME(self):
        return 'vqqlist'

    def _download(self, targetid):
        danmu_json = None
        timestamp = 0
        empty_count = 0
        while(True):
            url = "https://mfm.video.qq.com/danmu?otype=json&target_id=%s&timestamp=%s" % (targetid, timestamp)
            print('Start download: "%s".' % url)
            try:
                with urllib.request.urlopen(url) as f:
                    body = f.read()
            except Exception as e:
                print(e)
                break
            try:
                cur_danmu_json = json.loads(body, strict=False)
            except Exception as e:
                print(e)
                break
            if danmu_json == None:
                danmu_json = cur_danmu_json
            else:
                try:
                    danmu_json["count"] += cur_danmu_json["count"]
                    danmu_json["comments"].extend(cur_danmu_json["comments"])
                except Exception as e:
                    print(e)
                    break
                if cur_danmu_json["count"] == 0:
                    empty_count += 1
                    if empty_count > 10:
                        print("Section download finished: %s" % targetid)
                        break
            timestamp += 30
        return json.dumps(danmu_json, ensure_ascii=False).encode(encoding='utf-8')

    def download(self, line):
        line_res = []
        line_params = line.strip('\n').split('\t')
        targetid = line_params[0]
        filename = line_params[1]
        res = self._download(targetid=targetid)
        item_res = {}
        item_res['filename'] = filename + '.' + self.DANMU_EXTNAME
        item_res['data'] = res
        line_res.append(item_res)
        return line_res


if __name__ == '__main__':
    pass
else:
    from danmu_utils.common.plugin_collection import add_download_tool
    add_download_tool(VqqDownloader().DANMU_TYPE, VqqDownloader)