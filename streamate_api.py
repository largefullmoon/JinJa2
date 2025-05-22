import requests
from lxml import etree

SMLIVE_URL = "http://affiliate.streamate.com/SMLive/SMLResult.xml"

def get_performers(
    max_results=10,
    stream_type="live",
    min_age=None,
    max_age=None,
    ethnicity=None,
    fetishes=None,
    gender=None,
    keyword=None
):
    # Build XML request
    root = etree.Element("SMLQuery")
    options = etree.SubElement(root, "Options", MaxResults=str(max_results))
    available = etree.SubElement(root, "AvailablePerformers", QueryId="MyPythonQuery")
    include = etree.SubElement(available, "Include")
    etree.SubElement(include, "Descriptions")
    etree.SubElement(include, "Media").text = "staticbiopic"
    constraints = etree.SubElement(available, "Constraints")
    etree.SubElement(constraints, "PublicProfile")
    etree.SubElement(constraints, "StreamType").text = stream_type

    if min_age or max_age:
        age = etree.SubElement(constraints, "Age")
        if min_age:
            age.set("Min", str(min_age))
        if max_age:
            age.set("Max", str(max_age))
    if ethnicity:
        etree.SubElement(constraints, "Ethnicity").text = ethnicity
    if fetishes:
        etree.SubElement(constraints, "Fetishes").text = fetishes
    if gender:
        etree.SubElement(constraints, "Gender").text = gender
    if keyword:
        etree.SubElement(constraints, "Keyword").text = keyword

    xml_data = etree.tostring(root, xml_declaration=True, encoding="UTF-8")

    # Send request
    headers = {"Content-Type": "text/xml"}
    response = requests.post(SMLIVE_URL, data=xml_data, headers=headers, timeout=10)
    response.raise_for_status()

    # Parse XML response
    performers = []
    tree = etree.fromstring(response.content)
    for performer in tree.xpath("//Performer"):
        performer_id = performer.get("Id")
        performers.append({
            "id": performer_id,
            "name": performer.get("Name"),
            "age": performer.get("Age"),
            "ethnicity": performer.get("Ethnicity"),
            "fetishes": performer.get("Fetishes"),
            "gender": performer.get("Gender"),
            "stream_type": performer.get("StreamType"),
            "about": performer.findtext("Descriptions/About"),
            "turnons": performer.findtext("Descriptions/TurnOns"),
            "thumb_url": (performer.find("Media/Pic/Thumb").get("Src") if performer.find("Media/Pic/Thumb") is not None else None),
            "full_img_url": (performer.find("Media/Pic/Full").get("Src") if performer.find("Media/Pic/Full") is not None else None),
            "chat_url": f"https://www.streamate.com/cam/{performer_id}",
        })
    return performers