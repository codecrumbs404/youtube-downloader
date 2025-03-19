import yt_dlp
import json

def handler(request):
    try:
        # Parse incoming JSON data from the request
        data = request.json()

        # Extract the video URL and choice from the request
        video_url = data.get('video_url')
        choice = data.get('choice')

        # Initialize the options dictionary for yt_dlp
        ydl_opts = {}

        if choice == "1":  # Both video and audio
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
            ydl_opts['merge_output_format'] = 'mp4'
            print("Downloading best quality video and audio in MP4 format...")

        elif choice == "2":  # Video only
            ydl_opts['format'] = 'bestvideo/best'
            ydl_opts['merge_output_format'] = 'mp4'
            print("Downloading best quality video in MP4 format...")

        elif choice == "3":  # Audio only
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
            ydl_opts['extractaudio'] = True
            print("Downloading best quality audio in MP3 format...")

        else:
            return json.dumps({"error": "Invalid choice. Exiting."})

        # Set output template to save with video title as the filename
        ydl_opts['outtmpl'] = '/tmp/%(title)s.%(ext)s'  # Temporary storage location for serverless function

        # Create an instance of yt_dlp with the options and download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return json.dumps({"message": "Download completed successfully!"})

    except Exception as e:
        return json.dumps({"error": f"An error occurred: {str(e)}"})
