from twisted.web import static, resource
import qwebirc.util as util
# TODO: fix GZIP
#  from adminengine import AdminEngineAction
#  import pprint
try:
    from twisted.web.server import GzipEncoderFactory
    GZIP_ENCODER = GzipEncoderFactory()
except ImportError:
    GZIP_ENCODER = None

# TODO, cache gzip stuff
cache = {}


def clear_cache():
    global cache
    cache = {}


class StaticEngine(static.File):
    isLeaf = False
    hit = util.HitCounter()

    def __init__(self, *args, **kwargs):
        static.File.__init__(self, *args, **kwargs)

    def render(self, request):
        self.hit(request)
# temporarily disabled -- seems to eat big pages
#        if GZIP_ENCODER:
#            request._encoder = GZIP_ENCODER.encoderForRequest(request) # HACK
        return static.File.render(self, request)

    @property
    def adminEngine(self):
        return {
            #  "GZip cache": [
            #    ("Contents: %s" % pprint.pformat(list(cache.keys())),)# AdminEngineAction("clear", d))
            #  ],
            "Hits": [
                (self.hit,),
            ]
        }

    def directoryListing(self):
        return resource.ForbiddenResource()
