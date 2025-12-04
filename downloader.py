from pytube import YouTube
import os


def fetch_video(url):
    """Return a dict with metadata and stream lists for the given YouTube URL."""
    yt = YouTube(url)
    info = {
        "yt": yt,
        "title": yt.title,
        "length": yt.length,
        "author": yt.author,
        "views": yt.views,
        "thumbnail_url": yt.thumbnail_url,
        "video_streams": [s for s in yt.streams.filter(file_extension="mp4")],
        "audio_streams": [s for s in yt.streams.filter(only_audio=True)],
    }
    # convenience lists
    info["video_resolutions"] = [s.resolution for s in info["video_streams"]]
    info["video_itags"] = [s.itag for s in info["video_streams"]]
    info["audio_abrs"] = [s.abr for s in info["audio_streams"]]
    return info


def download_stream(yt, *, itag=None, only_audio=False, output_path=".", progress_callback=None):
    """Download a stream. If only_audio True it will download the first audio stream.

    - `yt` is a pytube.YouTube instance.
    - `itag` if provided selects that stream by itag.
    - `progress_callback(stream, chunk, bytes_remaining)` will be registered on the YouTube object.
    - returns full path of downloaded file.
    """
    if progress_callback:
        yt.register_on_progress_callback(progress_callback)

    if only_audio:
        stream = yt.streams.filter(only_audio=True).first()
    elif itag is not None:
        stream = yt.streams.get_by_itag(itag)
    else:
        stream = yt.streams.filter(file_extension="mp4").first()

    if not stream:
        raise RuntimeError("No matching stream found to download")

    out = stream.download(output_path=output_path)

    # if audio, optionally rename to .mp3 for convenience (no re-encoding)
    if only_audio:
        base, ext = os.path.splitext(out)
        new = base + ".mp3"
        try:
            os.rename(out, new)
            out = new
        except OSError:
            # ignore rename errors and keep original file
            pass

    return out
