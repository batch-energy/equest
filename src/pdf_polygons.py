import os
import sys
import PyPDF2
from collections import defaultdict
from itertools import chain


class PdfFile(object):
    def __init__(self, path):
        self.path = path
        self.pages = []
        self.name = os.path.split(os.path.abspath(path))[-1]
        reader = PyPDF2.PdfFileReader(open(path, "rb"))
        for index in range(reader.getNumPages()):
            page = Page(self, index, reader)

    @property
    def annotations(self):
        return list(chain(*(page.annotations for page in self.pages)))

    def __repr__(self):
        return f"<PdfFile: {self.name} - {len(self.pages)} pages>"


class Page(object):
    def __init__(self, pdf_file, index, reader):
        self.pdf_file = pdf_file
        self.index = index
        self.number = index + 1
        self.annotations = []
        pdf_file.pages.append(self)
        annots = reader.getPage(self.index).get("/Annots", [])
        if isinstance(annots, list):
            for annot in annots:
                annotation = Annotation(self, annot.getObject())

    def __repr__(self):
        return f"<Page {self.number} {self.pdf_file.name}>"


class Annotation(object):
    def __init__(self, page, annotation):
        self.page = page
        self.annotation = annotation
        page.annotations.append(self)

    def get(self, name):
        value = (self.annotation.get("/" + name) or "").strip()
        if value.startswith("("):
            value = value[1:]
        if value.endswith(")"):
            value = value[:-1]
        return value

    def __repr__(self):
        return (
            f'<Annotation {self.get("Subtype")[1:]} on Page {self.page.number}>'
        )


class PdfInputFile(object):
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.floors = []
        for page in pdf_file.pages:
            floor = Floor(self, page)


class Floor(object):
    def __init__(self, pdf_input_file, page):
        self.pdf_input_file = pdf_input_file
        self.page = page
        pdf_input_file.floors.append(self)
        self.polygons = []
        for annotation in page.annotations:
            if annotation.get("Subtype") == "/Polygon":
                polygon = Polygon(self, annotation)

    @property
    def name(self):
        pass

    @property
    def polygon_floors(self):
        counter = defaultdict(int)
        for polygon in self.polygons:
            counter[polygon.name] += 1
        return counter


class Polygon(object):
    def __init__(self, floor, annotation):
        self.floor = floor
        self.annotation = annotation
        floor.polygons.append(self)

    @property
    def activity(self):
        if self.activity_field is not None:
            return self.annotation.get(self.activity_field)
        else:
            return ""

    @property
    def name(self):
        if self.name_field is not None:
            return self.annotation.get(self.name_field)
        else:
            return ""

    @property
    def name_field(self):
        if len(self.annotation.get("T").split("-")) == 2:
            return "T"
        elif len(self.annotation.get("Subj").split("-")) == 2:
            return "Subj"
        else:
            return None

    @property
    def activity_field(self):
        if self.name_field == "T":
            return "Subj"
        elif self.name_field == "Subj":
            return "T"
        else:
            return None

    @property
    def area(self):
        self.annotation.get("Contents") or None


def main():
    path = sys.argv[1]
    pdf_file = PdfFile(path)
    pdf_input_file = PdfInputFile(pdf_file)
    for floor in pdf_input_file.floors:
        print(floor.polygon_floors)
        for polygon in floor.polygons:
            print(polygon.name)


def _():
    annotations = defaultdict(list)
    for i in range(1, input.getNumPages() + 1):
        annots = input.getPage(i - 1).get("/Annots", [])
        if not isinstance(annots, list):
            continue
        for annot in annots:
            annotations[i].append(annot.getObject())

    by_page = defaultdict(list)
    by_activity = defaultdict(list)
    nones = []
    print("\nRaw Data\n========================================")
    for page, annotations in annotations.items():
        for annotation in annotations:
            subtype = annotation.get("/Subtype")
            name = annotation.get("/T")
            activity = annotation.get("/Subj")
            if subtype != "/Polygon" or (name is None):
                continue
            area_str = annotation.get("/Contents")
            if area_str is not None and " ft" in area_str:
                area_str = float(area_str[:-4].replace(",", ""))
                try:
                    area = float(area_str)
                    by_page[page].append(area)
                    by_activity[activity].append(area)
                except:
                    area = "<None>"
                    nones.append(name)
            else:
                area = "<None>"
                nones.append(name)
            print(page, name, activity, area)

    print("\nBy Page\n========================================")
    for page, areas in by_page.items():
        print(f"  {page} {round(sum(areas), 2)}")

    print("\nBy Activity\n========================================")
    for page, areas in by_activity.items():
        print(f"  {page} {round(sum(areas), 2)}")

    if nones:
        print("\n\n  WARNING: Area could not be calculated for the following:")
        for name in nones:
            print(f"    {name}")


if __name__ == "__main__":
    main()
