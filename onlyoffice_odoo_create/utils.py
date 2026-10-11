"""Génération de fichiers Office (OOXML) vierges, en mémoire.

Aucune dépendance externe : on assemble le minimum de parties XML qu'un
fichier .docx / .xlsx / .pptx valide doit contenir, puis on zippe. Ces
fichiers s'ouvrent tels quels dans ONLYOFFICE (et Word/Excel/PowerPoint),
prêts à être édités et sauvegardés via le connecteur onlyoffice_odoo.

Ce module ne dépend PAS d'Odoo — il est importable et testable seul.
"""

import io
import zipfile

MIMETYPES = {
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}

_XML = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
_NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"
_NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
_NS_ODOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def _zip(parts):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        # [Content_Types].xml en premier, comme le veut la convention OPC.
        for name in sorted(parts, key=lambda n: (n != "[Content_Types].xml", n)):
            z.writestr(name, parts[name])
    return buf.getvalue()


# ── DOCX ──────────────────────────────────────────────────────────────────────
def _docx():
    parts = {
        "[Content_Types].xml": (
            f'{_XML}<Types xmlns="{_NS_CT}">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            "</Types>"
        ),
        "_rels/.rels": (
            f'{_XML}<Relationships xmlns="{_NS_REL}">'
            f'<Relationship Id="rId1" Type="{_NS_ODOC}/officeDocument" Target="word/document.xml"/>'
            "</Relationships>"
        ),
        "word/document.xml": (
            f'{_XML}<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            "<w:body><w:p/><w:sectPr/></w:body></w:document>"
        ),
    }
    return _zip(parts)


# ── XLSX ──────────────────────────────────────────────────────────────────────
def _xlsx():
    parts = {
        "[Content_Types].xml": (
            f'{_XML}<Types xmlns="{_NS_CT}">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            "</Types>"
        ),
        "_rels/.rels": (
            f'{_XML}<Relationships xmlns="{_NS_REL}">'
            f'<Relationship Id="rId1" Type="{_NS_ODOC}/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>"
        ),
        "xl/workbook.xml": (
            f'{_XML}<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            f'xmlns:r="{_NS_ODOC}">'
            '<sheets><sheet name="Feuille1" sheetId="1" r:id="rId1"/></sheets></workbook>'
        ),
        "xl/_rels/workbook.xml.rels": (
            f'{_XML}<Relationships xmlns="{_NS_REL}">'
            f'<Relationship Id="rId1" Type="{_NS_ODOC}/worksheet" Target="worksheets/sheet1.xml"/>'
            "</Relationships>"
        ),
        "xl/worksheets/sheet1.xml": (
            f'{_XML}<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            "<sheetData/></worksheet>"
        ),
    }
    return _zip(parts)


# ── PPTX ──────────────────────────────────────────────────────────────────────
_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
_P = "http://schemas.openxmlformats.org/presentationml/2006/main"

_EMPTY_TREE = (
    "<p:spTree>"
    '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
    "<p:grpSpPr><a:xfrm>"
    '<a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
    '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/>'
    "</a:xfrm></p:grpSpPr></p:spTree>"
)

_THEME = (
    f'{_XML}<a:theme xmlns:a="{_A}" name="Office">'
    "<a:themeElements>"
    '<a:clrScheme name="Office">'
    '<a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>'
    '<a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>'
    '<a:dk2><a:srgbClr val="44546A"/></a:dk2>'
    '<a:lt2><a:srgbClr val="E7E6E6"/></a:lt2>'
    '<a:accent1><a:srgbClr val="4472C4"/></a:accent1>'
    '<a:accent2><a:srgbClr val="ED7D31"/></a:accent2>'
    '<a:accent3><a:srgbClr val="A5A5A5"/></a:accent3>'
    '<a:accent4><a:srgbClr val="FFC000"/></a:accent4>'
    '<a:accent5><a:srgbClr val="5B9BD5"/></a:accent5>'
    '<a:accent6><a:srgbClr val="70AD47"/></a:accent6>'
    '<a:hlink><a:srgbClr val="0563C1"/></a:hlink>'
    '<a:folHlink><a:srgbClr val="954F72"/></a:folHlink>'
    "</a:clrScheme>"
    '<a:fontScheme name="Office">'
    '<a:majorFont><a:latin typeface="Calibri Light"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
    '<a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>'
    "</a:fontScheme>"
    '<a:fmtScheme name="Office">'
    "<a:fillStyleLst>"
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    "</a:fillStyleLst>"
    "<a:lnStyleLst>"
    '<a:ln w="6350" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
    '<a:ln w="12700" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
    '<a:ln w="19050" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
    "</a:lnStyleLst>"
    "<a:effectStyleLst>"
    "<a:effectStyle><a:effectLst/></a:effectStyle>"
    "<a:effectStyle><a:effectLst/></a:effectStyle>"
    "<a:effectStyle><a:effectLst/></a:effectStyle>"
    "</a:effectStyleLst>"
    "<a:bgFillStyleLst>"
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    "</a:bgFillStyleLst>"
    "</a:fmtScheme>"
    "</a:themeElements></a:theme>"
)


def _pptx():
    parts = {
        "[Content_Types].xml": (
            f'{_XML}<Types xmlns="{_NS_CT}">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/ppt/presentation.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
            '<Override PartName="/ppt/slideMasters/slideMaster1.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
            '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
            '<Override PartName="/ppt/slides/slide1.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            '<Override PartName="/ppt/theme/theme1.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
            "</Types>"
        ),
        "_rels/.rels": (
            f'{_XML}<Relationships xmlns="{_NS_REL}">'
            f'<Relationship Id="rId1" Type="{_NS_ODOC}/officeDocument" Target="ppt/presentation.xml"/>'
            "</Relationships>"
        ),
        "ppt/presentation.xml": (
            f'{_XML}<p:presentation xmlns:a="{_A}" xmlns:r="{_NS_ODOC}" xmlns:p="{_P}">'
            '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
            '<p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst>'
            '<p:sldSz cx="12192000" cy="6858000"/>'
            '<p:notesSz cx="6858000" cy="9144000"/>'
            "</p:presentation>"
        ),
        "ppt/_rels/presentation.xml.rels": (
            f'{_XML}<Relationships xmlns="{_NS_REL}">'
            f'<Relationship Id="rId1" Type="{_NS_ODOC}/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
            f'<Relationship Id="rId2" Type="{_NS_ODOC}/slide" Target="slides/slide1.xml"/>'
            f'<Relationship Id="rId3" Type="{_NS_ODOC}/theme" Target="theme/theme1.xml"/>'
            "</Relationships>"
        ),
        "ppt/slideMasters/slideMaster1.xml": (
            f'{_XML}<p:sldMaster xmlns:a="{_A}" xmlns:r="{_NS_ODOC}" xmlns:p="{_P}">'
            f"<p:cSld>{_EMPTY_TREE}</p:cSld>"
            '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
            'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" '
            'hlink="hlink" folHlink="folHlink"/>'
            '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
            "</p:sldMaster>"
        ),
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": (
            f'{_XML}<Relationships xmlns="{_NS_REL}">'
            f'<Relationship Id="rId1" Type="{_NS_ODOC}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
            f'<Relationship Id="rId2" Type="{_NS_ODOC}/theme" Target="../theme/theme1.xml"/>'
            "</Relationships>"
        ),
        "ppt/slideLayouts/slideLayout1.xml": (
            f'{_XML}<p:sldLayout xmlns:a="{_A}" xmlns:r="{_NS_ODOC}" xmlns:p="{_P}" type="blank" preserve="1">'
            f'<p:cSld name="Vierge">{_EMPTY_TREE}</p:cSld>'
            "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>"
            "</p:sldLayout>"
        ),
        "ppt/slideLayouts/_rels/slideLayout1.xml.rels": (
            f'{_XML}<Relationships xmlns="{_NS_REL}">'
            f'<Relationship Id="rId1" Type="{_NS_ODOC}/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
            "</Relationships>"
        ),
        "ppt/slides/slide1.xml": (
            f'{_XML}<p:sld xmlns:a="{_A}" xmlns:r="{_NS_ODOC}" xmlns:p="{_P}">'
            f"<p:cSld>{_EMPTY_TREE}</p:cSld>"
            "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>"
            "</p:sld>"
        ),
        "ppt/slides/_rels/slide1.xml.rels": (
            f'{_XML}<Relationships xmlns="{_NS_REL}">'
            f'<Relationship Id="rId1" Type="{_NS_ODOC}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
            "</Relationships>"
        ),
        "ppt/theme/theme1.xml": _THEME,
    }
    return _zip(parts)


_BUILDERS = {"docx": _docx, "xlsx": _xlsx, "pptx": _pptx}


def build_blank(fmt):
    """Retourne les octets d'un fichier Office vierge pour `fmt` (docx/xlsx/pptx)."""
    try:
        return _BUILDERS[fmt]()
    except KeyError as err:
        raise ValueError(f"Format non supporté : {fmt!r}") from err
