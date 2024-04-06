from flask import Flask, Response, request, jsonify
from modules.JSONHandler import JSONHandler
from modules.XMLHandler import XMLHandler
from modules.XMLValidator import XMLValidator


app = Flask(__name__)
app.config["VALIDATE_XML"] = True


@app.route("/json_to_xml", methods=["POST"])
def json_to_xml():
    input_json = request.get_json()
    parsed_xml = JSONHandler(input_json).handle_data(ret_XML=True)
    if app.config["VALIDATE_XML"]:
        validator = XMLValidator("modules/templates/Add_Entrant_List.xsd")
        if not validator.validate_xml_string(parsed_xml):
            return "The resulting XML is invalid", 418
    return Response(parsed_xml, mimetype="application/xml")


@app.route("/xml_to_json", methods=["POST"])
def xml_to_json():
    if request.content_type != "application/xml":
        return "Content isn't XML", 415
    xml = request.data.decode("utf-8")
    if app.config["VALIDATE_XML"]:
        validator = XMLValidator("modules/templates/Get_Entrant_List.xsd")
        if not validator.validate_xml_string(xml):
            return "The input XML is invalid", 418
    return XMLHandler(xml).handle_data()


if __name__ == "__main__":
   app.run()
