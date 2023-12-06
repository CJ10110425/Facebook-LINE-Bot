import requests
import os
import dotenv


def fetch_facebook_likes(access_token, video_ids):
    """
    Fetches likes counts for given Facebook video IDs.

    Parameters:
    access_token (str): Access token for Facebook Graph API.
    video_ids (dict): A dictionary mapping video IDs to their respective names.

    Returns:
    dict: A dictionary with team names and their corresponding likes counts.
    """
    likes_counts = {}

    for video_id, team_name in video_ids.items():
        url = f'https://graph.facebook.com/v18.0/{video_id}/likes?summary=true&access_token={access_token}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            likes_count = data['summary']['total_count']
            likes_counts[team_name] = likes_count
        else:
            print(
                f"Error fetching likes for video ID {video_id}: {response.text}")

    return likes_counts


def display_sorted_likes(likes_counts):
    """
    Creates and returns a string representing the sorted likes counts.

    Parameters:
    likes_counts (dict): A dictionary with team names and their corresponding likes counts.

    Returns:
    str: A string representation of the sorted likes counts.
    """
    sorted_likes_counts = sorted(
        likes_counts.items(), key=lambda x: x[1], reverse=True)

    likes_display = ""
    rank = 1
    for team_name, likes in sorted_likes_counts:
        rank_label = f"Rank {rank}"
        likes_display += f"{rank_label}: {team_name},{likes}\n"
        rank += 1

    return likes_display.strip()  # Remove trailing newline


def fetch_facebook_likes_users(access_token, object_id):
    """
    Fetches a list of users who liked a given Facebook post or video.

    Parameters:
    access_token (str): Access token for Facebook Graph API.
    object_id (str): The ID of the Facebook post or video.

    Returns:
    list: A list of user names who liked the post or video.
    """
    users_who_liked = []
    url = f'https://graph.facebook.com/v18.0/{object_id}/likes?access_token={access_token}'

    while True:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            users_who_liked.extend([user['name']
                                   for user in data.get('data', [])])

            # Check if there is a next page
            if 'next' in data.get('paging', {}):
                url = data['paging']['next']
            else:
                break
        else:
            print(
                f"Error fetching likes for object ID {object_id}: {response.text}")
            break

    return users_who_liked


if __name__ == "__main__":
    dotenv.load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')
    video_ids = {
        '1032184421373970': 'FRIGPATHY',
        '896707631835497': 'GaiaBit毛焦點靚青春',
        '884820739683019': 'JLL',
        '357195453630410': 'Vitawear 戴命醫電',
        '994616074971005': '捷足AgileFoot',
        '751091986837645': '運動揪揪',
        '909824847528125': '嘿疲YOLO乳'
    }
    likes_counts = fetch_facebook_likes(access_token, video_ids)
    print("\n")
    print(display_sorted_likes(likes_counts))
    # object_id = '1032184421373970'  # Replace with the actual post/video ID
    # users = fetch_facebook_likes_users(access_token, object_id)
    # print(users)
