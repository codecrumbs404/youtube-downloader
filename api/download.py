import yt_dlp
import json

def handler(request):
    try:
        # Parse the JSON data from the frontend request
        data = request.json()
        video_url = data.get('video_url')
        choice = data.get('choice')

        # Prepare options based on the choice
        ydl_opts = {}

        if choice == "1":  # Both video and audio
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
            ydl_opts['merge_output_format'] = 'mp4'
            result_message = "Downloading best quality video and audio in MP4 format..."

        elif choice == "2":  # Video only
            ydl_opts['format'] = 'bestvideo/best'
            ydl_opts['merge_output_format'] = 'mp4'
            result_message = "Downloading best quality video in MP4 format..."

        elif choice == "3":  # Audio only
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
            ydl_opts['extractaudio'] = True
            result_message = "Downloading best quality audio in MP3 format..."

        else:
            return json.dumps({'error': 'Invalid choice'})

        ydl_opts['outtmpl'] = '%(title)s.%(ext)s'

        # Start downloading using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return json.dumps({'message': result_message})

    except Exception as e:
        return json.dumps({'error': str(e)})
