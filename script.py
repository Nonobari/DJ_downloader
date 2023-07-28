import sys
from pytube import YouTube, Playlist
from pytube.cli import on_progress
from pytube.helpers import safe_filename
from tqdm import tqdm

def get_highest_audio(url, path = "music"):
    video = YouTube(url, on_progress_callback=on_progress)
    # Download the highest audio resolution save it in mp3 format and make a progress bar
    print("downloading....")
    file_name = f"{safe_filename(f'{video.title} - {video.author}')}.wav"
    video.streams.filter(only_audio = True).order_by('abr').desc().first().download(output_path= path, filename=file_name)
    print("Downloaded! :)")

def download_playlist(url, path = "music"):
    playlist = Playlist(url)
    n = len(playlist.videos)
    print(f"Number of videos in playlist: {n}")
    for video in tqdm(playlist.videos):
        try :
            # remove impossible characters from the title
            file_name = f"{safe_filename(f'{video.title} - {video.author}')}.wav"
            video.streams.filter(only_audio = True).order_by('abr').desc().first().download(output_path= path, filename=file_name)
            
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            sys.exit(1)
        except:
            print(f"Error downloading {file_name}")

def main():
    if len(sys.argv) < 2:
        print("Please provide a link")
        sys.exit(1)
    elif len(sys.argv) == 2:
        if "playlist" in sys.argv[1]:
            download_playlist(sys.argv[1])
        elif "watch" in sys.argv[1]:
            get_highest_audio(sys.argv[1])
    elif len(sys.argv) == 3:
        if "playlist" in sys.argv[1]:
            download_playlist(sys.argv[1], f"music/{sys.argv[2]}")
        elif "watch" in sys.argv[1]:
            get_highest_audio(sys.argv[1], f"music/{sys.argv[2]}")


if __name__ == "__main__":
    main()