#!/usr/bin/env python
"""
Inkscape plugin: delete the selected object(s) and any objects on top of them.

I.E. delete the selected element(s) and any other elements that are completely
within the bounding-boxes of the selected elements that have a greater z-order

Simply put, you select a "background" rectangle, then use this plugin to
delete it and everything that appears on top of it.
"""

import sys
import collections
import subprocess
import os
import pprint

# inkscape specific
sys.path.extend(['/usr/share/inkscape/extensions',
                 '/Applications/Inkscape.app/Contents/Resources/extensions'])
import inkex


Point = collections.namedtuple('Point', ['x', 'y'])

Box = collections.namedtuple('Box', ['tl', 'tr', 'br', 'bl'])
# tl=top left, tr=top right, br=bottom right, bl=bottom left

ElementInfo = collections.namedtuple('ElementInfo',
                                     ['x', 'y', 'width', 'height'])


def contains(outer, inner):
    """ Return true if the Box inner is completely within the Box outer """
    return inner.tl.x >= outer.tl.x and inner.tl.y >= outer.tl.y and \
           inner.br.x <= outer.br.x and inner.br.y <= outer.br.y


class DeleteAboveEffect(inkex.Effect):
    """ Delete the selected element and everything above it """
    element_info = None

    def load_element_info(self):
        """ Ask inkscape for information about all object bounding boxes """
        element_info = dict()
        command = ['inkscape', '--query-all', self.svg_file]
        check_output = subprocess.check_output

        with open(os.devnull, 'w') as null:
            for line in check_output(command, stderr=null).splitlines():
                raw_id, raw_x, raw_y, raw_width, raw_height = line.split(',')
                element_info[raw_id] = ElementInfo(float(raw_x),
                                                   float(raw_y),
                                                   float(raw_width),
                                                   float(raw_height))

        self.element_info = element_info
        return

    def remove(self, element):
        """ Remove the specified element from the document tree """
        parent = self.getParentNode(element)
        if parent is None:
            return
        parent.remove(element)

    def bbox(self, element):
        """ Return the bounding-box of the given element """
        element_id = element.attrib['id']
        info = self.element_info[element_id]
        x = info.x
        y = info.y
        width = info.width
        height = info.height

        return Box(Point(x, y),
                   Point(x + width, y),
                   Point(x + width, y + height),
                   Point(x, y + height))

    def effect(self):
        """
        For every selected element, remove it and all items on top of it
        """
        self.load_element_info()
        elements_to_remove = list()

        for selected_element in self.selected.itervalues():
            selected_element_bbox = self.bbox(selected_element)
            elements_to_remove.append(selected_element)

            # search the document tree for the selected element
            # when found, every subsequent element will be "above" it.
            # (i.e. svg documents draw from the background up, so a background
            # element will appear first, then elements that are progressively
            # closer to the viewer will appear subsequently in the svg file)
            found_selected_element = False
            for element in self.document.getiterator():
                if not found_selected_element:
                    if element == selected_element:
                        found_selected_element = True
                    continue
                # Hereafter we are iterating over all elements above the
                # selected element. We need to delete them if they appear to
                # be "on top of" the selection (i.e. within the bounding box
                # of the selection)
                try:
                    element_bbox = self.bbox(element)
                except KeyError:
                    continue
                if contains(selected_element_bbox, element_bbox):
                    elements_to_remove.append(element)

        # Now we remove the items we've previously found. Search and remove
        # need to be separate bulk steps because tree search is disrupted by
        # tree modification
        for condemned_element in set(elements_to_remove):
            self.remove(condemned_element)


if __name__ == '__main__':
    if False:
        # Some tools for debug use
        PPRINTER = pprint.PrettyPrinter(indent=4)
        FMT = PPRINTER.pformat
        DUMP = lambda obj: inkex.debug(FMT(obj))

    EFFECT = DeleteAboveEffect()
    EFFECT.affect()
