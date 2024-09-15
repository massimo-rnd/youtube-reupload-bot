import os
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import googleapiclient.http

API_KEY = 'YOUR_YOUTUBE_API_KEY'
CHANNEL_ID = 'SOURCE_CHANNEL_ID'
CLIENT_SECRETS_FILE = "client_secrets.json"

def get_latest_video(channel_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=1,
        order="date"
    )
    response = request.execute()
    latest_video = response['items'][0]['id']['videoId']
    return latest_video

def download_video(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    os.system(f"yt-dlp {url}")
    return f"{video_id}.mp4"

def upload_video_to_youtube(video_file, title, description, tags, category_id):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes)
    credentials = flow.run_console()
    youtube = build("youtube", "v3", credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=googleapiclient.http.MediaFileUpload(video_file)
    )
    response = request.execute()
    return response

if __name__ == "__main__":
    latest_video_id = get_latest_video(CHANNEL_ID, API_KEY)
    video_file = download_video(latest_video_id)
    upload_response = upload_video_to_youtube(
        video_file,
        "Title for the new upload",
        "Description for the new upload",
        ["tag1", "tag2"],
        "22"  # Category ID for People & Blogs
    )
    print(upload_response)
