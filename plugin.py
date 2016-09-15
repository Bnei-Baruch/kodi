import sys
import urllib
import urlparse

import xbmcgui
import xbmcplugin


def build_url(query):
    base_url = sys.argv[0]

    return base_url + '?' + urllib.urlencode(query)


def build_items_list(items):
    items_list = []

    for item in items:
        li = xbmcgui.ListItem(label=items[item]['title'], thumbnailImage=items[item]['album_cover'])
        li.setProperty('fanart_image', items[item]['album_cover'])
        li.setProperty('IsPlayable', 'true')
        url = build_url({'mode': 'stream', 'url': items[item]['url'], 'title': items[item]['title']})
        items_list.append((url, li, False))

    xbmcplugin.addDirectoryItems(addon_handle, items_list, len(items_list))
    xbmcplugin.setContent(addon_handle, 'video')
    xbmcplugin.endOfDirectory(addon_handle)


def play(url):
    play_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)


def build_content():
    items = {}
    index = 1

    items.update(
        {index: {'album_cover': '', 'title': 'Radio Zohar', 'url': 'http://icecast.kab.tv/radiozohar2014.mp3'}})

    items.update({2: {'album_cover': '', 'title': 'Channel 66',
                      'url': 'http://edge1.il.kab.tv/rtplive/tv66-heb-high.stream/playlist.m3u8'}})

    items.update({3: {'album_cover': '', 'title': 'Sviva Tova',
                      'url': 'http://edge1.uk.kab.tv/rtplive/live1-cn4qdiwU-heb-medium.stream/playlist.m3u8'}})

    return items


def main():
    args = urlparse.parse_qs(sys.argv[2][1:])
    mode = args.get('mode', None)

    if mode is None:
        content = build_content()
        build_items_list(content)
    elif mode[0] == 'stream':
        play(args['url'][0])


if __name__ == '__main__':
    addon_handle = int(sys.argv[1])
    main()
