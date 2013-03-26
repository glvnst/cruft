#!/usr/bin/python
"""
wx - Report weather conditions for yahoo WOEIDs
"""
import xml.dom.minidom as minidom
import urllib2
import sys


class DumbXML(object):
    """
    A simple wrapper for urllib2 and xml.dom.minidom designed to get
    attributes from tag elements in an XML document. Access tags by attribute
    name, e.g.: dxml.meta.charset
    """
    namespace = None
    dom = None

    class Node(object):
        """
        Class designed to contain a minidom node that can answer
        getAttribute. Accesses are via attribute names.
        """
        node = None

        def __init__(self, node):
            self.node = node

        def __getattr__(self, attr_name):
            """
            Call getAttribute on the wrapped XML node with the given argument
            """
            return self.node.getAttribute(attr_name)

    def __init__(self, source_url, namespace="*"):
        """
        Init with the xml document at source_url, optionally select specified
        namespace
        """
        self.namespace = namespace
        data = urllib2.urlopen(source_url)
        self.dom = minidom.parseString(data.read())

    def __getattr__(self, tag_name):
        """ Return the first xml tag element matching tag_name """
        element_list = self.dom.getElementsByTagNameNS(self.namespace,
                                                       tag_name)
        return self.Node(element_list[0])


def direction_string(direction):
    """
    Return a direction string from a numeric direction spec. E.G.: 3 -> N
    """
    bounded_direction = divmod(direction, 360)[1]
    directions = ((0.0,   "N"), (22.5,  "NNE"), (45.0,  "NE"), (67.5,  "ENE"),
                  (90.0,  "E"), (112.5, "ESE"), (135.0, "SE"), (157.5, "SSE"),
                  (180.0, "S"), (202.5, "SSW"), (225.0, "SW"), (247.5, "WSW"),
                  (270.0, "W"), (292.5, "WNW"), (315.0, "NW"), (337.5, "NNW"),
                  (360.0, "N"))
    # I made a faster version, but I like this one better
    diffs = [(abs(bounded_direction - deg), name) for deg, name in directions]
    return sorted(diffs)[0][1]


if __name__ == '__main__':
    import argparse

    ARGP = argparse.ArgumentParser(
        description='Report the current weather for yahoo WOEID(s)')
    ARGP.add_argument('-u', '--units', choices=['c', 'f'],
                      help='report in Celsius or Fahrenheit',
                      default='c')  # I <3 Freija
    ARGP.add_argument('woeid', nargs="+", help='yahoo WOEID(s) to report on')
    ARGS = ARGP.parse_args()

    if sys.stdout.encoding is None:
        import codecs
        OUT = codecs.getwriter('utf8')(sys.stdout)
    else:
        OUT = sys.stdout

    for woeid in ARGS.woeid:
        url = 'http://weather.yahooapis.com/forecastrss?w={}&u={}'.format(
            woeid, ARGS.units)
        wx = DumbXML(url)
        wind_direction = direction_string(int(wx.wind.direction))
        OUT.write(
            (u"{0.location.city}, {0.location.region} "
             "as of {0.condition.date}\n"

             "{3} {0.condition.text}, {0.condition.temp}{2} "
             "{0.units.temperature} (low {0.forecast.low}{2} "
             "{0.units.temperature} / high {0.forecast.high}{2} "
             "{0.units.temperature})\n"

             "{3} {0.wind.speed} {0.units.speed} winds, "
             "heading {1}\n"

             "{3} {0.atmosphere.humidity}% humidity, "
             "barometer @ {0.atmosphere.pressure} {0.units.pressure}\n"

             "{3} {0.atmosphere.visibility} {0.units.distance} visibility\n"

             "{3} Sunrise @ {0.astronomy.sunrise} / "
             "Sunset @ {0.astronomy.sunset}\n").format(wx,
                                                       wind_direction,
                                                       u'\N{DEGREE SIGN}',
                                                       u'\N{BULLET}'))
