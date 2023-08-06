from abc import ABC


class Media(ABC):
    def __init__(self, redis_host: str, source: str) -> None:
        import redis
        _redishost = redis_host.split(":")
        _host = _redishost[0]
        _port = int(_redishost[1]) if len(_redishost) > 1 else 6379
        _db = int(_redishost[2]) if len(_redishost) > 2 else 0
        self._redis = redis.Redis(host=_host, port=_port, db=_db)
        self._table = {"root": "media", "index": "_idx",
                       "running": "_rkey", "update": "_upd"}
        self._source = source
        pass

    def get_table(self, type: str, opt: str = "") -> str:
        if opt != "":
            return f"{self._table['root']}:{self._table[opt]}:{type}"
        return f"{self._table['root']}:{type}"

    def get_uid(self, type: str, value: str, sourcecol: str = None, source: str = None, addnew: bool = True) -> tuple:
        _source = source if source is not None else self._source
        if sourcecol is None:
            _table = self.get_table(type, "index")
        else:
            _table = "{}{}:{}".format(self.get_table(
                type, "index"), "" if _source == "" else f":{_source}", sourcecol)
        _, _uids = self._redis.zscan(name=_table, match=value)
        if _uids != []:
            return int(_uids[0][1]), False
        if addnew:
            _uid = self._redis.incr(name=self.get_table(type, "running"))
            self._redis.zadd(name=self.get_table(
                type, "index"), mapping={value: _uid})
            return _uid, True
        return None, False

    def _to_str(self, data: dict) -> str:
        import json
        return json.dumps(data)

    def _to_dict(self, data: str) -> dict:
        import json
        return json.loads(data)

    def _sysdate(self, date: str = None) -> float:
        import time
        from datetime import datetime
        if date is None:
            _now = datetime.now()
        else:
            _now = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return time.mktime(_now.timetuple())

    def add(self, type: str, data, col: str = None, uidcol: str = None, excl: list = [], group: dict = {}, inclsource: bool = True, sourceidx: list = []) -> bool:
        _group = ":".join([_g for _g, _ in group.items()])
        _group = ":" + _group if group != {} else ""

        _data = data if isinstance(data, list) else [data]
        _now = self._sysdate()
        for _d in _data:
            _d = self._conv_data(_d)
            if col is None:
                _val = _d
                _mod_d = _d
            else:
                _val = _d.get(col)
                _mod_d = _d.copy()
                for _x in excl:
                    _not_exist = "~!missing~!"
                    if _mod_d.get(_x, _not_exist) != _not_exist:
                        _mod_d.pop(_x)
            # if isinstance(_mod_d, dict):
            #     for _k, _v in group.items():
            #         _mod_d.update({_k: _v})
            _d_excl_idx = _d.copy()
            for _k, _ in _d.items():
                if _k[-1] == "_":
                    _d_excl_idx.pop(_k)
                    _mod_d.pop(_k)
            if uidcol is None:
                _uid, _ = self.get_uid(type=type, value=_val)
                try:
                    _d_comp = {}
                    for _s in self.get(type=type, uid=_uid, source=self._source, incluid=False):
                        _d_comp = _s
                        break
                    if _d == _d_comp:
                        continue
                except Exception as e:
                    print("error:", e)
                    pass
            else:
                _uid = _d.get(uidcol)
            if inclsource:
                self._redis.hset(
                    name=f"{self.get_table(type)}:{self._source}:{_uid}", mapping=_d_excl_idx)
            self._redis.hset(
                name=f"{self.get_table(type)}:{_uid}", mapping=_mod_d)
            self._redis.zadd(name=self.get_table(
                type, "index"), mapping={_val: _uid})
            for _k, _v in _d.items():
                if _k[-1] == "_":
                    _col = _k[:-1].split("|")
                    _search = _col[1] if len(_col) > 1 else _col[0]
                    _col = _col[0]
                    if inclsource:
                        _tbl = "{}:{}:{}".format(self.get_table(
                            type, "index"), self._source, _search)
                    else:
                        if _search == "":
                            _tbl = self.get_table(type, "index")
                        else:
                            _tbl = "{}:{}".format(self.get_table(
                                type, "index"), _search)
                    self._redis.zadd(name=_tbl, mapping={_v: _uid})
            for _x in excl:
                if inclsource:
                    _tbl = "{}:{}:{}".format(self.get_table(
                        type, "index"), self._source, _x)
                else:
                    _tbl = "{}:{}".format(self.get_table(
                        type, "index"), _x)
                self._redis.zadd(name=_tbl, mapping={_d.get(_x): _uid})
            for _x in sourceidx:
                if isinstance(_x, str):
                    _tmp_source = self._source
                    _tmp_col = _x
                else:
                    _tmp_source = _x[0] if len(_x) > 1 else self._source
                    _tmp_col = _x[1] if len(_x) > 1 else _x
                _tbl = "{}:{}:{}".format(self.get_table(
                    type, "index"), _tmp_source, _tmp_col)
                self._redis.zadd(name=_tbl, mapping={_d.get(_tmp_col): _uid})
            for _k, _v in group.items():
                if _v is None:
                    continue
                self._redis.zadd(name="{}:{}:{}".format(self.get_table(
                    type, "index"), _k, _v), mapping={_val: _uid})
                self._redis.zadd(name="{}:{}".format(self.get_table(
                    type, "index"), _k), mapping={_uid: _v})
            self._redis.zadd(name=self.get_table(
                type, "update"), mapping={_uid: _now})
        return True

    def _zscan(self, type: str = None, match: str = "*", table: str = None, kcol: str = "key", vcol: str = "value", wildcard: bool = True) -> list:
        if type is None and table is None:
            return []
        _table = table if table is not None else self.get_table(type, "index")
        _match = match if match == "*" else f"*{match}*" if wildcard else match
        _, _idx = self._redis.zscan(name=_table, match=_match)
        _rtn = []
        for _v, _k in _idx:
            _rtn.append({kcol: int(_k), vcol: _v.decode("UTF-8")})
        return _rtn

    def _hgetall(self, type: str = None, uid: str = None, table: str = None, source: bool = False) -> dict:
        if type is None and table is None:
            return {}
        _table = table if table is not None else "{}{}:{}".format(
            self.get_table(type), f":{self._source}" if source else "", uid)
        return {_k.decode("UTF-8"): _v.decode("UTF-8") for _k, _v in self._redis.hgetall(name=_table).items()}

    def _get_last(self, type: str = None, table: str = None, page: int = 0, count: int = None) -> list:
        count = count if count is not None else 50
        if type is None and table is None:
            return []
        _table = table if table is not None else self.get_table(type, "update")
        _rtn = [int(_c.decode("UTF-8")) for _c in self._redis.zrevrangebyscore(
            name=_table, min=0, max=9999999999, start=page * count, num=count)]
        return _rtn

    def _conv_data(self, data: dict) -> dict:
        return {_k: _v if not isinstance(_v, bool) else 1 if _v else 0 for _k, _v in data.items() if not isinstance(_v, list) if _v is not None}

    def get(self, type: str, value: str = None, uid: list = [], count: int = None, source: bool = False, incluid: bool = True):
        count = count if count is not None else 50
        _rtn = []
        _uid = uid
        if _uid == []:
            if value is None:
                _uid = self._get_last(type=type, count=count)
            else:
                _uid = [_u.get("uid") for _u in self._zscan(
                    type=type, match="*" if value is None else value, kcol="uid")]
        _uid = _uid if isinstance(_uid, list) else [_uid]
        for _u in _uid:
            _data = self._hgetall(type=type, uid=_u, source=source)
            if incluid:
                _data.update({"uid": _u})
            _rtn.append(_data)
        return _rtn

    def cats(self, cat: str = None, uid: str = None, count: int = None):
        if uid is not None:
            _rtn = self.get(type="cats", uid=[uid], count=count)
        else:
            _rtn = self.get(type="cats", value=cat, count=count)
        return _rtn

    def scats(self, scat: str = None, uid: str = None, cat: str = None, catuid: str = None, count: int = None):
        _rtn = []
        if uid is not None:
            _rtn = self.get(type="scats", uid=[uid], count=count)
        elif scat is not None:
            _rtn = self.get(type="scats", value=cat, count=count)
        elif cat is not None or catuid is not None:
            _catsuid = [_c.get("uid") for _c in self.cats(
                cat=cat, uid=catuid, count=count)]

            _scatsuid = []
            _idxtbl = "{}:{}".format(self.get_table(
                type="scats", opt="index"), "cat")
            for _u in _catsuid:
                _scatsuid += [_i.get("key")
                              for _i in self._zscan(type="scats", table=f"{_idxtbl}:{_u}")]
            _scats = []
            for _s in self._get_last(type="scats", count=count):
                if _s in _scatsuid:
                    _scats.append(_s)

            _rtn = self.get(
                type="scats", uid=_scats, count=count)
        else:
            _rtn = self.get(type="scats", count=count)
        return _rtn

    def people(self, person: str = None, uid: str = None, video: str = None, videouid: str = None, count: int = None):
        _rtn = []
        if uid is not None:
            _rtn = self.get(type="people", uid=[uid], count=count)
        elif person is not None:
            _rtn = self.get(type="people", value=person, count=count)
        else:
            if video is not None or videouid is not None:
                if videouid is not None:
                    _vlst = self.get(type=self._source, uid=[
                                     videouid], count=count)
                else:
                    _vlst = self.get(type=self._source,
                                     value=video, count=count)
                _idxtbl = "{}:{}".format(self.get_table(
                    type="people", opt="index"), self._source)
                for _v in _vlst:
                    _plst = [_i.get(
                        "key") for _i in self._zscan(table="{}:{}".format(_idxtbl, _v.get("uid")))]
                    if _plst != []:
                        _rtn = self.get(type="people", uid=_plst, count=count)
                    break
            else:
                _rtn = self.get(type="people", count=count)
        return _rtn

    def videos(self, video: str = None, uid: str = None, people: str = None, peopleuid: str = None, scat: str = None, scatuid: str = None, cat: str = None, catuid: str = None, count: int = None, hvsourceonly: bool = True):
        _rtn = []
        _vuid = []
        if video is not None or uid is not None:
            if uid is not None:
                _vlst = self.get(type="videos", uid=[uid], count=count)
            else:
                _vlst = self.get(type="videos", value=video, count=count)
            _vuid = [_v.get("uid") for _v in _vlst]
        else:
            if scat is not None or scatuid is not None or cat is not None or catuid is not None:
                _scatsuid = [_s.get("uid") for _s in self.scats(scat=scat, uid=scatuid,
                                                                cat=cat, catuid=catuid)]
                _idxtbl = "{}:{}".format(self.get_table(
                    type=self._source, opt="index"), "scat")
                _suid = []
                for _u in _scatsuid:
                    _suid += [_i.get("key")
                              for _i in self._zscan(table=f"{_idxtbl}:{_u}")]
                _vuid = [_s.get("tmdb_id")
                         for _s in self.get(type=self._source, uid=_suid)]
                # print(_vuid)
            elif people is not None or peopleuid is not None:
                _peopleuid = [_p.get("uid") for _p in self.people(
                    person=people, uid=peopleuid)]
                _idxtbl = "{}:{}".format(self.get_table(
                    self._source, "index"), "people")
                _vlst = []
                for _u in _peopleuid:
                    _vlst += [_i.get("key")
                              for _i in self._zscan(table=f"{_idxtbl}:{_u}")]
                _vlst = list(set(_vlst))
                _vuid = [_v.get("tmdb_id")
                         for _v in self.get(type=self._source, uid=_vlst)]
                # _vuid = [_p.get("tmdb_id")
                #          for _p in self.get(type=self._source, uid=_puid)]
            else:
                _count = max(
                    100, 50 if count is None else count) if hvsourceonly else count
                _vuid = self._get_last(type="videos", count=_count)
        for _v in self.get(type="videos", uid=_vuid):
            _idxtbl = "{}:{}".format(self.get_table(
                type=self._source, opt="index"), "tmdb_id")
            _sinfo = {}
            _vuid = _v.get("uid")
            _suid = [_i.get("key")
                     for _i in self._zscan(table=f"{_idxtbl}:{_vuid}")]
            for _s in _suid:
                _sinfo = self._hgetall(type=self._source, uid=_s)
                _people = self.people(videouid=_s)
                if _people != {}:
                    _v.update({"people": _people})
                break
            if hvsourceonly and _sinfo == {}:
                continue
            if _sinfo != {}:
                _v.update({self._source: _sinfo})
            _rtn.append(_v)

        return _rtn

    def add_cats(self, cats: list):
        self.add(type="cats", data=cats, col="cat", excl=["id"])

    def add_scats(self, scats: list, cat: str):
        _uid, _ = self.get_uid(type="cats", value=cat,
                               sourcecol="id", addnew=False)
        if _uid is not None:
            self.add(type="scats", data=scats, col="scat",
                     excl=["id"], group={"cat": _uid})

    def add_videos(self, videos: dict, scat: str, tmdb_id: str):
        videos = self._conv_data(videos)
        _scat_uid, _ = self.get_uid(type="scats", value=scat,
                                    sourcecol="id", addnew=False)
        _tmdb_uid = None
        _group = {}
        if tmdb_id is not None:
            _tmdb_uid, _ = self.get_uid(
                type="videos", value=tmdb_id, sourcecol="tmdb_id", source="", addnew=False)
        else:
            _title = videos.get("title")
            _tmdb_uid, _ = self.get_uid(
                type="videos", value=_title, addnew=False)
        # videos.update({"id_": videos.get("id")})
        # _group.update({"id": videos.get("id")})
        _name = videos.get("title")
        _tail = videos.get("tail", None)
        if _tail is not None:
            _name = "{} ({})".format(_name, _tail)

        videos.update({"name": _name})
        if _tmdb_uid is not None:
            videos.update({"tmdb_id": _tmdb_uid})
            _group.update({"tmdb_id": _tmdb_uid})
        if _scat_uid is not None:
            _group.update({"scat": _scat_uid})
        self.add(type=self._source, data=videos, col="name",
                 group=_group, inclsource=False, sourceidx=["id"])

    def add_tmdb_videos(self, data):
        _data = data if isinstance(data, list) else [data]
        for _d in _data:
            _d = self._conv_data(_d)
            _group = {}
            if _d.get("release_date", None) is not None:
                try:
                    _group.update(
                        {"year": str(int(_d.get("release_date")[:4]))})
                except:
                    pass
            _tmdb_id = _d.get("id", None)
            if _tmdb_id is not None:
                _d.update({"tmdb_id": _tmdb_id})
                _d.pop("id")
            if _d.get("original_title", None) is not None:
                _d.update({"original_title|_": _d.get("original_title")})
            _sid = _d.get(self._source, None)
            if _sid is not None:
                _group.update({self._source: _sid})
            self.add(type="videos", data=_d, col="title", group=_group,
                     excl=["tmdb_id"], inclsource=False)

    def add_tmdb_people(self, data, vid: str):
        _data = data if isinstance(data, list) else [data]
        _group = {}
        _vid_uuid, _ = self.get_uid(type=self._source, value=vid,
                                    sourcecol="id", addnew=False)
        if _vid_uuid is not None:
            _group.update({self._source: _vid_uuid})
        _mod_data = []
        for _d in _data:
            _d = self._conv_data(_d)
            _d.update({"oth_name": _d.get("oth_name", _d.get("name"))})
            _d.update({"name|_": _d.get("name")})
            if _vid_uuid is not None:
                _d.update({self._source: _vid_uuid})
            _mod_data.append(_d)
        self.add(type="people", data=_mod_data, col="oth_name", excl=[self._source],
                 group=_group, inclsource=False)

    def add_video_people_index(self, video):
        _vid = video.get("id")
        _vuid, _ = self.get_uid(
            type=self._source, value=_vid, sourcecol="id", addnew=False)
        _video = self.get(type=self._source, uid=[_vuid])[0]
        for _p in self._zscan(table="{}:{}:{}".format(
                self.get_table(type="people", opt="index"), self._source, _vuid)):
            self._redis.zadd(name="{}:{}:{}".format(self.get_table(
                type=self._source, opt="index"), "people", _p.get("key")), mapping={_video.get("title"): _vuid})

        # print(video, actors, directors)
