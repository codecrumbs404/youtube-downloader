import json
import yt_dlp

def handler(request):
    try:
        # Parse the incoming request body as JSON
        data = request.json
        video_url = data.get('video_url')
        choice = int(data.get('choice'))

        if not video_url:
            return json.dumps({"error": "No video URL provided"}), 400

        # Set up yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best' if choice == 3 else 'best',
            'outtmpl': '/tmp/%(title)s.%(ext)s',  # Save to /tmp for Vercel deployment
        }

        # Download the video or audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)

        # Return a success message
        return json.dumps({"message": "Download successful", "title": info_dict.get('title')}), 200

    except Exception as e:
        # Return an error message if something goes wrong
        return json.dumps({"error": f"An error occurred: {str(e)}"}), 500
