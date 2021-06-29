"""
All API queries, parsing, and formatting functions are stored in this file
This project use the TMD API.
"""
import os
import requests

API_KEY = os.environ.get("API_KEY")


# Queries
def query_data(query_type, keyword, category=None):
    """Will look for all types"""
    if query_type == "id":
        url = f"https://api.themoviedb.org/3/{category}/{keyword}?api_key={API_KEY}" \
              f"&append_to_response=credits,videos,recommendations"
    elif query_type == "title":
        url = f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={keyword}"
    else:
        return None
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    return response.json()


def query_seasons(series_id, season_number):
    url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}?api_key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    return response.json()


# Parse and formats
def parse_query_by_title(response):
    """ Will return the data used in search movie for the query by title"""
    parsed_response = {
        "movies": [],
        "series": []
    }
    if not response:
        return response

    for result in response["results"]:
        if "movie" in result["media_type"]:
            movie_dict = media_template(result)
            movie_dict["release_date"] = result["release_date"]
            parsed_response["movies"].append(movie_dict)
        elif "tv" in result["media_type"]:
            series_dict = media_template(result)
            parsed_response["series"].append(series_dict)

    return parsed_response


def parse_detail_by_id(response, media_type):
    """ Will return the data used in search movie for the query by id"""
    parsed_response = {
        "media": {},
        "actors": [],
        "recommendations": [],
        "videos": [],
        "seasons": []
    }

    if not response or not media_type:
        return parsed_response

    media_dict = media_template(response)
    if media_type == "movie":
        media_dict["release_date"] = response["release_date"]
    parsed_response["media"] = media_dict

    for recommendation in response["recommendations"]["results"]:
        recommendations_dict = media_template(recommendation)
        if "movie" in recommendation["media_type"]:
            recommendations_dict["release_date"] = recommendation["release_date"]
        parsed_response["recommendations"].append(recommendations_dict)

    for video in response["videos"]["results"]:
        videos_dict = {
            "name": video["name"],
            "key": video["key"],
            "site": video["site"]
        }
        parsed_response["videos"].append(videos_dict)

    for actor in response["credits"]["cast"]:
        actors_dict = {
            "id": actor["id"],
            "name": actor["name"],
            "character": actor["character"],
            "profile_path": actor["profile_path"]
        }
        parsed_response["actors"].append(actors_dict)

    if "seasons" in response:
        for season in response["seasons"]:
            season_dict = media_template(season)
            season_dict["season_number"] = season["season_number"]
            season_dict["episodes"] = []
            episodes = query_seasons(response["id"], season["season_number"])
            for episode in episodes["episodes"]:
                episodes_dict = media_template(episode)
                episodes_dict["episode_number"] = episode["episode_number"]
                season_dict["episodes"].append(episodes_dict)
            parsed_response["seasons"].append(season_dict)

    return parsed_response


# HELPERS
def media_template(r):
    return {
        "id": r["id"],
        "title": r["original_title"] if "original_title" in r else r["title"] if "title" in r else r["original_name"]
        if "original_name" in r else r["name"] if "name" in r else "",
        "poster_path": r["poster_path"] if "poster_path" in r else r["still_path"] if "still_path" in r else "",
        "backdrop_path": r["backdrop_path"] if "backdrop_path" in r else "",
        "overview": r["overview"] if "overview" in r else "",
        "media_type": r["media_type"] if "media_type" in r else "",
        "vote_average": r["vote_average"] if "vote_average" in r else ""
    }
