# yt_master_tool.py
from pytubefix import Search, Playlist, YouTube
from pytubefix.cli import on_progress
from pytubefix.contrib.search import Search, Filter


def search_videos(query):
    print("🔎 Recherche de vidéos sur YouTube...\n")
    results = Search(query)
    for video in results.videos:
        print(f"🎬 Titre : {video.title}")
        print(f"🔗 URL : {video.watch_url}")
        print(f"⏱️ Durée : {video.length} secondes")
        print("---")

def search_videos_with_filters():
    print("🔎 Recherche de vidéos avec filtres...\n")
    
    # Configuration des filtres
    print("🛠️ Configurez vos filtres :")
    upload_date = input("📅 Date de publication (Today/This week/This month/This year) : ") or None
    video_type = input("🎥 Type de contenu (Video/Channel/Playlist) : ") or None
    duration = input("⏱️ Durée (Short/Under 4 minutes/Long/Over 20 minutes) : ") or None
    quality = input("📹 Qualité (4K/HD/None) : ") or None
    license_type = input("🔓 Licence (Creative Commons/Standard) : ") or None
    sort_by = input("🔀 Trier par (Relevance/Upload date/View count/Rating) : ") or None

    # Création du dictionnaire de filtres
    filters = {}
    if upload_date:
        filters['upload_date'] = Filter.get_upload_date(upload_date)
    if video_type:
        filters['type'] = Filter.get_type(video_type)
    if duration:
        filters['duration'] = Filter.get_duration(duration)
    if quality:
        filters['features'] = [Filter.get_features(quality)]
    if license_type:
        filters['features'] = filters.get('features', []) + [Filter.get_features(license_type)]
    if sort_by:
        filters['sort_by'] = Filter.get_sort_by(sort_by)

    # Lancement de la recherche
    query = input("🔍 Entrez le terme de recherche : ")
    s = Search(query, filters=filters)
    
    print("🎬 Résultats de la recherche :\n")
    for video in s.videos:
        print(f"🎥 Titre : {video.title}")
        print(f"🔗 URL : {video.watch_url}")
        print(f"⏱️ Durée : {video.length} secondes")
        print("---")

def download_playlist_audio(playlist_url):
    print("📥 Téléchargement de la playlist audio...\n")
    try:
        # Validation de l'URL
        if "list=" not in playlist_url:
            raise ValueError("❌ L'URL fournie n'est pas une URL de playlist valide.")

        # Création de l'objet Playlist
        pl = Playlist(playlist_url)
        
        # Téléchargement des vidéos
        for video in pl.videos:
            print(f"🎶 Téléchargement : {video.title}")
            ys = video.streams.get_audio_only()
            ys.download()

        print("✅ Tous les fichiers audio ont été téléchargés avec succès !")

    except ValueError as ve:
        print(f"Erreur : {ve}")
    except Exception as e:
        print(f"❌ Une erreur est survenue : {e}")

def download_audio(video_url):
    print("🎧 Téléchargement d'une vidéo en audio...\n")
    yt = YouTube(video_url, on_progress_callback=on_progress)
    print(f"🎬 Vidéo : {yt.title}")
    ys = yt.streams.get_audio_only()
    ys.download()
    print("✅ Téléchargement terminé !")

from pytubefix import YouTube
from pytubefix.cli import on_progress

def download_video(video_url):
    print("📥 Téléchargement de la vidéo en haute résolution...\n")
    try:
        # Initialisation de YouTube avec l'URL et la barre de progression
        yt = YouTube(video_url, on_progress_callback=on_progress)
        print(f"🎬 Titre de la vidéo : {yt.title}")
        
        # Obtenir le flux avec la plus haute résolution
        ys = yt.streams.get_highest_resolution()
        print("🚀 Téléchargement en cours...")
        ys.download()
        print("✅ Téléchargement terminé avec succès !")

    except Exception as e:
        print(f"❌ Une erreur est survenue lors du téléchargement : {e}")

# Menu principal
def main():
    print("✨ Bienvenue dans l'outil YouTube Downloader avec PyTubeFix ✨")
    while True:
        print("\nQue souhaitez-vous faire ?")
        print("1️⃣ Rechercher des vidéos sur YouTube")
        print("2️⃣ Rechercher des vidéos avec filtres")
        print("3️⃣ Télécharger une playlist audio")
        print("4️⃣ Télécharger l'audio d'une vidéo spécifique")
        print("5️⃣ Télécharger la vidéo en haute résolution")
        print("6️⃣ Quitter")
        choice = input("👉 Votre choix : ")

        if choice == '1':
            query = input("🔍 Entrez le terme de recherche : ")
            search_videos(query)
        elif choice == '2':
            search_videos_with_filters()
        elif choice == '3':
            playlist_url = input("🔗 Entrez l'URL de la playlist : ")
            download_playlist_audio(playlist_url)
        elif choice == '4':
            video_url = input("🔗 Entrez l'URL de la vidéo : ")
            download_audio(video_url)
        elif choice == '5':
            video_url = input("🔗 Entrez l'URL de la vidéo : ")
            download_video(video_url)
        elif choice == '6':
            print("👋 Au revoir !")
            break        
        else:
            print("❌ Choix invalide. Réessayez.")

if __name__ == "__main__":
    main()
