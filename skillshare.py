import requests, json, sys, re, os
from slugify import slugify

class Skillshare(object):

    def __init__(
        self,
        cookie='device_session_id=f9aa76bf-0aea-49f1-9d5e-97638027f830; first_landing=utm_campaign%3D%26utm_source%3D%28direct%29%26utm_medium%3D%28none%29%26referrer%3D%26referring_username%3D; __pdst=d4adba231b7f4fc383668b99c7db6fe3; loc=%7B%22lat%22%3A%2260.1699%22%2C%22lng%22%3A%2224.9384%22%2C%22cid%22%3A%2266%22%2C%22city_name%22%3A%22Helsinki%22%2C%22city_district%22%3A%22%22%2C%22region%22%3Anull%2C%22region_code%22%3Anull%2C%22country_code%22%3A%22FI%22%2C%22country%22%3A%22Finland%22%7D; PHPSESSID=3238c17166588730ea6fd6580c0943b7; YII_CSRF_TOKEN=QjBUVWdqWHBndnMxMm0zM0VraVFUMnRibm1hQVhNS0EJlnHHVZsbcE1orZT1PaDK5ocE-11CgpjYS4tBOavqJw%3D%3D; show-like-copy=0; visitor_tracking=utm_campaign%3D%26utm_source%3D%28direct%29%26utm_medium%3D%28none%29%26referrer%3D%26referring_username%3D; orientation-flow-data=%7B%22orientationPath%22%3A%7B%22orientation%5C%2Findex%22%3A%22orientation%5C%2Ffollowskills%22%2C%22orientation%5C%2Ffollowskills%22%3A%22orientation%5C%2Fclasses%22%2C%22orientation%5C%2Fclasses%22%3A%22orientation%5C%2Freferrals%22%2C%22orientation%5C%2Freferrals%22%3A%22orientation%5C%2Fcomplete%22%7D%2C%22viewedPages%22%3A%5B%5D%2C%22finalRedirect%22%3A%22https%3A%5C%2F%5C%2Fwww.skillshare.com%5C%2Fhome%3Fvia%3Dlogged-in-home%22%2C%22completesOrientation%22%3Atrue%2C%22force%22%3Atrue%7D; __utma=99704988.1520436739.1574401554.1574401554.1574401554.1; __utmc=99704988; __utmz=99704988.1574401554.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=99704988.|1=visitor-type=user=1; __utmt=1; __utmb=99704988.1.10.1574401554; _gcl_au=1.1.1630272359.1574401555; _fbp=fb.1.1574401555715.350889659; __stripe_mid=07cf7cf4-96ce-47c5-8505-bdcd6e004273; __stripe_sid=7f2e0b41-d703-4931-8f3a-dc0cf3e0aec3; pses={"id":"qxtcijow4xh","start":1574401556741,"last":1574401556744}; IR_gbd=skillshare.com; IRMS_la4650=1574401557607; mp_c0ffa2093d02e0d503db07fe142aab98_mixpanel=%7B%22distinct_id%22%3A%20%2216e91a544fd357-0ca23bd683bfe8-2393f61-100200-16e91a544fe517%22%2C%22%24device_id%22%3A%20%2216e91a544fd357-0ca23bd683bfe8-2393f61-100200-16e91a544fe517%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24user_id%22%3A%20%2216e91a544fd357-0ca23bd683bfe8-2393f61-100200-16e91a544fe517%22%7D; G_ENABLED_IDPS=google; _scid=e75ad2ec-645c-4b40-b7a7-f76e8e22fc6b; __ssid=91916ab2126099c09831cff13d57fa3; _sctr=1|1574361000000; ss_hide_default_banner=1574401573.772',
        download_path=os.environ.get('FILE_PATH', './Skillshare'),
        pk='BCpkADawqM2OOcM6njnM7hf9EaK6lIFlqiXB0iWjqGWUQjU7R8965xUvIQNqdQbnDTLz0IAO7E6Ir2rIbXJtFdzrGtitoee0n1XXRliD-RH9A-svuvNW9qgo3Bh34HEZjXjG4Nml4iyz3KqF',
        brightcove_account_id=3695997568001,
    ):
        # self.cookie = cookie.strip().strip('"')
        self.cookie = cookie
        # print(f'self.cookie: {self.cookie}')
        self.download_path = download_path
        self.pk = pk.strip()
        self.brightcove_account_id = brightcove_account_id
        self.pythonversion = 3 if sys.version_info >= (3, 0) else 2

    def is_unicode_string(self, string):
        if (self.pythonversion == 3 and isinstance(string, str)) or (self.pythonversion == 2 and isinstance(string, unicode)):
            return True

        else:
            return False

    def download_course_by_url(self, url):
        m = re.match('https://www.skillshare.com/classes/.*?/(\\d+)', url)
        assert m, 'Failed to parse class ID from URL'
        self.download_course_by_class_id(m.group(1))

    def download_course_by_class_id(self, class_id):
        data = self.fetch_course_data_by_class_id(class_id=class_id)
        teacher_name = None
        if 'vanity_username' in data['_embedded']['teacher']:
            teacher_name = data['_embedded']['teacher']['vanity_username']
        if not teacher_name:
            teacher_name = data['_embedded']['teacher']['full_name']
        assert teacher_name, 'Failed to read teacher name from data'
        if self.is_unicode_string(teacher_name):
            teacher_name = teacher_name.encode('ascii', 'replace')
        title = data['title']
        if self.is_unicode_string(title):
            title = title.encode('ascii', 'replace')

        # self.teacher_name = slugify(teacher_name)
        # self.title = slugify(title)

        # base_path = os.path.abspath(os.path.join(self.download_path, slugify(teacher_name), slugify(title))).rstrip('/')
        base_path = os.path.abspath(os.path.join(self.download_path, slugify(title))).rstrip('/')
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        for u in data['_embedded']['units']['_embedded']['units']:
            for s in u['_embedded']['sessions']['_embedded']['sessions']:
                video_id = None
                if 'video_hashed_id' in s:
                    if s['video_hashed_id']:
                        video_id = s['video_hashed_id'].split(':')[1]
                    assert video_id, 'Failed to read video ID from data'
                    s_title = s['title']
                    if self.is_unicode_string(s_title):
                        s_title = s_title.encode('ascii', 'replace')
                    file_name = '{} - {}'.format(str(s['index'] + 1).zfill(2), slugify(s_title))
                    self.download_video(fpath='{base_path}/{session}.mp4'.format(base_path=base_path,
                      session=file_name),
                      video_id=video_id)
                    print('')

    def fetch_course_data_by_class_id(self, class_id):
        res = requests.get(url=('https://api.skillshare.com/classes/{}'.format(class_id)),
          headers={'Accept':'application/vnd.skillshare.class+json;,version=0.8',
         'User-Agent':'Skillshare/4.1.1; Android 5.1.1',
         'Host':'api.skillshare.com',
         'cookie':self.cookie})
        assert res.status_code == 200, 'Fetch error, code == {}'.format(res.status_code)
        return res.json()

    def download_video(self, fpath, video_id):
        meta_url = 'https://edge.api.brightcove.com/playback/v1/accounts/{account_id}/videos/{video_id}'.format(account_id=(self.brightcove_account_id),
          video_id=video_id)
        meta_res = requests.get(meta_url,
          headers={'Accept':'application/json;pk={}'.format(self.pk),
         'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
         'Origin':'https://www.skillshare.com'})
        assert not meta_res.status_code != 200, 'Failed to fetch video meta'
        for x in meta_res.json()['sources']:
            if 'container' in x:
                if x['container'] == 'MP4' and 'src' in x:
                    dl_url = x['src']
                    break

        print('Downloading {}...'.format(fpath))
        if os.path.exists(fpath):
            print('Video already downloaded, skipping...')
            return
        with open(fpath, 'wb') as (f):
            response = requests.get(dl_url, allow_redirects=True, stream=True)
            total_length = response.headers.get('content-length')
            if not total_length:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write('\r[%s%s]' % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()

            print('')
