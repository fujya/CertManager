#!/usr/bin/env python
# -*- encoding:utf8 -*-
import memcache

#memcached index key
indexkey = 1000

#set data to memcached
#initialize memecached
cachedata = 'cache data'
memcachedclient = memcache.Client(['127.0.0.1:11211'])
memcachedclient.flush_all()
memcachedclient.set(str(indexkey), cachedata,time=3600)

#get data from memcached
memcachedclient = memcache.Client(['127.0.0.1:11211'])
cacheddata = memcachedclient.get(str(indexkey))
print cacheddata
