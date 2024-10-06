#!/usr/bin/env python3

from pytube import YouTube
import sys



def print_html_md_code_for_youtube_card(URL: str, THUMBNAIL: str, TITLE: str, DURATION: str, ALIGN: str = 'left') -> None:
    print(f"<!-- {TITLE} -->")
    print(f"<div style=\"border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;\">")
    print(f"\t<a href=\"{URL}\" target=\"_blank\" style=\"display: block; position: relative;\">")
    print(f"\t\t<!--  Thumbnail -->")
    print(f"\t\t<img src=\"{THUMBNAIL}\" alt=\"YouTube Thumbnail\" style=\"width: 100%; display: block;\">")
    print(f"\t\t<!-- Play button in the center -->")
    print(f"\t\t<div style=\"position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;\">")
    print(f"\t\t\t<div style=\"width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;\"></div>")
    print(f"\t\t</div>")
    print(f"\t\t<!-- Black rectangle with duration at bottom-right -->")
    print(f"\t\t<div style=\"position: absolute; bottom: 8px; right: 8px; background: rgba(0, 0, 0, 0.8); color: white; padding: 2px 6px; font-size: 12px; border-radius: 3px;\">")
    print(f"\t\t\t{DURATION}")
    print(f"\t\t</div>")
    print(f"\t</a>")
    print(f"\t<div style=\"margin: 0 auto; width: 90%; text-align: {ALIGN};\">")
    print(f"\t\t<!-- Text of URL -->")
    print(f"\t\t<p style=\"margin: 10px 0;\"><a href=\"{URL}\" target=\"_blank\">{URL}</a></p>")
    print(f"\t\t<!-- Separation line -->")
    print(f"\t\t<hr style=\"border: 0; height: 1px; background: #ddd; margin: 10px 0;\">")
    print(f"\t\t<!-- Text of Title -->")
    print(f"\t\t<p style=\"margin: 10px 0;\"><a href=\"{URL}\" target=\"_blank\">{TITLE}</a></p>")
    print(f"\t</div>")
    print(f"</div>")
    print()




def autoget_youtube_video_info(URL: str) -> tuple[str, str, str]:
    """
    If the online resources are located, the function will return a tuple, containing:
    - The URL of the Thumbnail
    - The Title of the YouTube clip
    - The Duration of the YouTube clip
    """
    try:
        # Create a YouTube object
        yt = YouTube(URL)

        # Get YouTube clip info
        thumbnail_url: str = yt.thumbnail_url
        title: str = yt.title
        duration: int = yt.length  # Duration in seconds

        # Convert duration to a more readable format (D:HH:MM:SS)
        # Calculate days, hours, minutes, and seconds
        (days, remainder) = divmod(duration, 24*3600)   # 24*3600 seconds in a day
        (hours, remainder) = divmod(remainder, 3600)    # 3600 seconds in an hour
        (minutes, seconds) = divmod(remainder, 60)      # 60 seconds in a minute
        
        # Format duration as D:HH:MM:SS
        if int(days) > 0:
            duration_formatted = f"{days}:{hours:02}:{minutes:02}:{seconds:02}"
        elif int(hours) > 0:
            duration_formatted = f"{hours:02}:{minutes:02}:{seconds:02}"
        elif int(minutes) > 0:
            duration_formatted = f"{minutes:02}:{seconds:02}"
        else:
            duration_formatted = f"0:{seconds:02}"

        return (thumbnail_url, title, duration_formatted)
    except Exception as e:
        print(f"[ERROR] Something went wrong while retrieving YouTube information!", file=sys.stderr)
        print(f"[ERROR] {e}", file=sys.stderr)
        print(f"Please make sure the provided URL is from YouTube, the URL works and you have internet connection.")
        sys.exit(1)


def help_option() -> None:
    print("NAME:")
    print(f"\t{sys.argv[0]} - generates HTML / MarkDown code for a YouTube clickable card.")
    print()
    print(f"DESCRIPTION:")
    print(f"\t{sys.argv[0]} requires a single argument, the URL of the YouTube clip.")
    print(f"\tThe script will automatically fetch, from online, metadata (info) of the YouTube Video/Short,")
    print(f"\tincluding THUMBNAIL PICTURE's URL, TITLE, DURATION.")
    print()
    print(f"\tWithout internet connection, the script doesn't work.")
    print(f"\tIt will generate an error message.")
    print()
    print(f"\tThe generated HTML/MarkDown code will include a thumbnail, containing a white arrow in a red circle.")
    print(f"\tThe text of the URL will be rendered above the title, both being splitted by a line, and aligned to the left.")
    print(f"\tThe code will also include relevant comments.")
    print()
    print("USAGE:")
    print(f"\t$ {sys.argv[0]} $URL")
    print(f"\t$ {sys.argv[0]} --url=$URL")
    print()
    print(f"\t$ {sys.argv[0]} -h")
    print(f"\t$ {sys.argv[0]} --help")
    print()
    print("OPTIONS:")
    print("\t-h, --help     Display this suggestive help text and exit.")
    print(f"\t--url=        Pass the URL as value to this flag.")
    print()
    print("See more info at project home page: https://github.com/TrifanBogdan24/EmbedYT-Card-Generator.git")
    print()

def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Invalid number of arguments!", file=sys.stderr)
        print(f"[ERROR] The script expects a single argument!", file=sys.stderr)
        print(f"Please run '{sys.argv[0]} --help' to see the available options.", file=sys.stderr)
    else:
        if sys.argv[1] in ['-h', '--help']:
            help_option()
        else:
            URL = ''
            if sys.argv[1].startswith('--url='):
                URL = sys.argv[1].removeprefix('--url=')
            else:
                URL = sys.argv[1]
            
            (THUMBNAIL, TITLE, DURATION) = autoget_youtube_video_info(URL)
            print_html_md_code_for_youtube_card(
                URL, THUMBNAIL, TITLE, DURATION, ALIGN='left'
            )


if __name__ == '__main__':
    main()

