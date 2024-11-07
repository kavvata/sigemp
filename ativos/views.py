from datetime import datetime

from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework.views import Request

from ativos.models import Computer, Software
from ativos.parsers import ZlibXMLParser, XMLParser
from ativos.renderers import XMLRenderer
from ativos.serializer import ComputerSerializer


def get_softwares(pair):
    key, value = pair

    if key != "SOFTWARES":
        return False

    return True


# Create your views here.
@api_view(["GET"])
def fetch(request):
    return Response(ComputerSerializer(Computer.objects.all(), many=True).data)


class InventoryView(APIView):
    parser_classes = [ZlibXMLParser, XMLParser]
    renderer_classes = [XMLRenderer]




    def post(self, request: Request):
        data = request.data

        if "PROLOG" in data.get("QUERY"):
            return Response({"PROLOG_FREQ": "24", "RESPONSE": "SEND"})

        software_list = []

        # FIXME: lento demais
        # TODO: implementar transaction
        for software_data in data["CONTENT"]["SOFTWARES"]:
            try:
                install_date = datetime.strptime(software_data.get("INSTALLDATE"), "%d/%m/%Y")
            except TypeError:
                install_date = datetime.today()

            software, is_new = Software.objects.get_or_create(
                arch=software_data.get("ARCH"),
                guid=software_data.get("GUID"),
                name=software_data.get("NAME"),
                publisher=software_data.get("PUBLISHER"),
                version=software_data.get("VERSION"),
                install_date=install_date,
            )

            software_list.append(software)

        computer, is_new = Computer.objects.get_or_create(device_uid=data["DEVICEID"])

        if is_new:
            computer.save()

        computer.softwares.set(software_list)

        return Response(status=200)