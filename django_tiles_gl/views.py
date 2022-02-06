from nis import cat
from django.http import HttpResponse, JsonResponse
from landez import MBTilesReader,  ExtractionError

def tile(request, z, x, y):
    reader = MBTilesReader('../berlin.mbtiles')
    try:
        data = reader.tile(z, x, y)
        return HttpResponse(
            content=data,
            headers={
                'Content-Type': 'application/x-protobuf',
                'Content-Encoding': 'gzip',
            },
            status=200,
        )

    except ExtractionError:
        return HttpResponse(
            status=204,
        )

def metadata(request):
    reader = MBTilesReader('../berlin.mbtiles')

    return JsonResponse(reader.metadata())
