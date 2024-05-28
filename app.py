import os
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv

load_dotenv()
GENIUS_API_BASE_URL = "https://api.genius.com"
GENIUS_API_KEY = os.getenv("GENIUS_API_KEY")

if not GENIUS_API_KEY:
    raise ValueError("Genius API 키가 설정되지 않았습니다. 환경 변수 'GENIUS_API_KEY'를 설정하세요.")

def search_song_by_lyrics(query):
    headers = {
        "Authorization": f"Bearer {GENIUS_API_KEY}"
    }
    search_url = f"{GENIUS_API_BASE_URL}/search"
    params = {
        "q": query
    }
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        hits = response_data["response"]["hits"]
        songs = []
        for hit in hits:
            song_info = hit["result"]
            songs.append({
                "title": song_info["title"],
                "artist": song_info["primary_artist"]["name"]
            })
        return songs
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"API 요청 중 오류가 발생했습니다: {e}")
        return None
    except ValueError as e:
        messagebox.showerror("Error", f"응답을 처리하는 중 오류가 발생했습니다: {e}")
        return None

def search_song_by_title(title):
    headers = {
        "Authorization": f"Bearer {GENIUS_API_KEY}"
    }
    search_url = f"{GENIUS_API_BASE_URL}/search"
    params = {
        "q": title
    }
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        hits = response_data["response"]["hits"]
        songs = []
        for hit in hits:
            song_info = hit["result"]
            if title.lower() in song_info["title"].lower():
                songs.append({
                    "title": song_info["title"],
                    "artist": song_info["primary_artist"]["name"]
                })
        return songs
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"API 요청 중 오류가 발생했습니다: {e}")
        return None
    except ValueError as e:
        messagebox.showerror("Error", f"응답을 처리하는 중 오류가 발생했습니다: {e}")
        return None

def search_artist_by_name(artist_name):
    headers = {
        "Authorization": f"Bearer {GENIUS_API_KEY}"
    }
    search_url = f"{GENIUS_API_BASE_URL}/search"
    params = {
        "q": artist_name
    }
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        hits = response_data["response"]["hits"]
        artists = []
        for hit in hits:
            artist_info = hit["result"]["primary_artist"]
            artists.append({
                "name": artist_info["name"],
                "id": artist_info["id"]
            })
        return artists
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"API 요청 중 오류가 발생했습니다: {e}")
        return None
    except ValueError as e:
        messagebox.showerror("Error", f"응답을 처리하는 중 오류가 발생했습니다: {e}")
        return None

def get_songs_by_artist_id(artist_id):
    headers = {
        "Authorization": f"Bearer {GENIUS_API_KEY}"
    }
    search_url = f"{GENIUS_API_BASE_URL}/artists/{artist_id}/songs"
    params = {
        "per_page": 10,
        "page": 1
    }
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        songs = response_data["response"]["songs"]
        song_list = []
        for song in songs:
            song_list.append({
                "title": song["title"],
                "artist": song["primary_artist"]["name"]
            })
        return song_list
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"API 요청 중 오류가 발생했습니다: {e}")
        return None
    except ValueError as e:
        messagebox.showerror("Error", f"응답을 처리하는 중 오류가 발생했습니다: {e}")
        return None

class GeniusApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Search App")
        self.geometry("600x500")
        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self)

        self.song_lyrics_tab = ttk.Frame(self.tab_control)
        self.song_title_tab = ttk.Frame(self.tab_control)
        self.artist_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.song_lyrics_tab, text="가사로 노래 검색")
        self.tab_control.add(self.song_title_tab, text="노래 제목으로 검색")
        self.tab_control.add(self.artist_tab, text="아티스트로 검색")
        self.tab_control.pack(expand=1, fill="both")

        # 가사 검색 탭
        self.song_lyrics_label = ttk.Label(self.song_lyrics_tab, text="가사를 입력하세요")
        self.song_lyrics_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.song_lyrics_entry = ttk.Entry(self.song_lyrics_tab, width=50)
        self.song_lyrics_entry.grid(row=1, column=0, columnspan=2, pady=10)

        self.song_lyrics_button = ttk.Button(self.song_lyrics_tab, text="검색", command=self.search_songs_by_lyrics)
        self.song_lyrics_button.grid(row=2, column=0, pady=10)

        self.song_lyrics_clear_button = ttk.Button(self.song_lyrics_tab, text="초기화", command=self.clear_lyrics_results)
        self.song_lyrics_clear_button.grid(row=2, column=1, pady=10)

        self.song_lyrics_result = tk.Text(self.song_lyrics_tab, wrap="word", height=15)
        self.song_lyrics_result.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

        self.song_lyrics_tab.rowconfigure(3, weight=1)
        self.song_lyrics_tab.columnconfigure(0, weight=1)
        self.song_lyrics_tab.columnconfigure(1, weight=1)

        # 노래 제목 검색 탭
        self.song_title_label = ttk.Label(self.song_title_tab, text="노래 제목을 입력하세요")
        self.song_title_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.song_title_entry = ttk.Entry(self.song_title_tab, width=50)
        self.song_title_entry.grid(row=1, column=0, columnspan=2, pady=10)

        self.song_title_button = ttk.Button(self.song_title_tab, text="검색", command=self.search_songs_by_title)
        self.song_title_button.grid(row=2, column=0, pady=10)

        self.song_title_clear_button = ttk.Button(self.song_title_tab, text="초기화", command=self.clear_title_results)
        self.song_title_clear_button.grid(row=2, column=1, pady=10)

        self.song_title_result = tk.Text(self.song_title_tab, wrap="word", height=15)
        self.song_title_result.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

        self.song_title_tab.rowconfigure(3, weight=1)
        self.song_title_tab.columnconfigure(0, weight=1)
        self.song_title_tab.columnconfigure(1, weight=1)

        # 아티스트 검색 탭
        self.artist_label = ttk.Label(self.artist_tab, text="아티스트 이름을 입력하세요")
        self.artist_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.artist_entry = ttk.Entry(self.artist_tab, width=50)
        self.artist_entry.grid(row=1, column=0, columnspan=2, pady=10)

        self.artist_button = ttk.Button(self.artist_tab, text="검색", command=self.search_artists)
        self.artist_button.grid(row=2, column=0, pady=10)

        self.artist_clear_button = ttk.Button(self.artist_tab, text="초기화", command=self.clear_artist_results)
        self.artist_clear_button.grid(row=2, column=1, pady=10)

        self.artist_result = tk.Text(self.artist_tab, wrap="word", height=15)
        self.artist_result.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

        self.artist_tab.rowconfigure(3, weight=1)
        self.artist_tab.columnconfigure(0, weight=1)
        self.artist_tab.columnconfigure(1, weight=1)

    def search_songs_by_lyrics(self):
        query = self.song_lyrics_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "유효한 가사를 입력하세요.")
            return

        songs = search_song_by_lyrics(query)
        self.song_lyrics_result.delete(1.0, tk.END)

        if songs:
            for song in songs:
                self.song_lyrics_result.insert(tk.END, f"제목: {song['title']}, 아티스트: {song['artist']}\n")
        else:
            self.song_lyrics_result.insert(tk.END, "가사에 해당하는 노래를 찾지 못했습니다.")

    def search_songs_by_title(self):
        title = self.song_title_entry.get().strip()
        if not title:
            messagebox.showwarning("Warning", "유효한 노래 제목을 입력하세요.")
            return

        songs = search_song_by_title(title)
        self.song_title_result.delete(1.0, tk.END)

        if songs:
            for song in songs:
                self.song_title_result.insert(tk.END, f"제목: {song['title']}, 아티스트: {song['artist']}\n")
        else:
            self.song_title_result.insert(tk.END, "해당 제목의 노래를 찾지 못했습니다.")

    def search_artists(self):
        artist_name = self.artist_entry.get().strip()
        if not artist_name:
            messagebox.showwarning("Warning", "유효한 아티스트 이름을 입력하세요.")
            return

        artists = search_artist_by_name(artist_name)
        self.artist_result.delete(1.0, tk.END)

        if artists:
            for artist in artists:
                self.artist_result.insert(tk.END, f"이름: {artist['name']}\n")
                artist_songs = get_songs_by_artist_id(artist["id"])
                if artist_songs:
                    self.artist_result.insert(tk.END, "노래 목록:\n")
                    for song in artist_songs:
                        self.artist_result.insert(tk.END, f"  - 제목: {song['title']}, 아티스트: {song['artist']}\n")
        else:
            self.artist_result.insert(tk.END, "아티스트를 찾지 못했습니다.")

    def clear_lyrics_results(self):
        self.song_lyrics_entry.delete(0, tk.END)
        self.song_lyrics_result.delete(1.0, tk.END)

    def clear_title_results(self):
        self.song_title_entry.delete(0, tk.END)
        self.song_title_result.delete(1.0, tk.END)

    def clear_artist_results(self):
        self.artist_entry.delete(0, tk.END)
        self.artist_result.delete(1.0, tk.END)

if __name__ == "__main__":
    app = GeniusApp()
    app.mainloop()
