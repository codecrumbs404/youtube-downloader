from flask import Flask, request, jsonify
import yt_dlp
import json
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def handler():
    try:
        # Parse incoming JSON data from the request
        data = request.json

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
            return jsonify({"error": "Invalid choice. Exiting."})

        # Set output template to save with video title as the filename
        ydl_opts['outtmpl'] = '/tmp/%(title)s.%(ext)s'  # Temporary storage location for serverless function

        # Create an instance of yt_dlp with the options and download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return jsonify({"message": "Download completed successfully!"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


# Make sure to set the host and port for Glitch environment
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)))
