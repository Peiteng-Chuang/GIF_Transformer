import os
import sys
import vlc
import threading
import time

# 設置 VLC 的安裝路徑，這裡應該是包含所有 VLC DLL 文件的目錄
vlc_path='C:/Program Files/VideoLAN/VLC'
os.add_dll_directory(vlc_path)
sys.path.append(vlc_path)
stop_playback = False

def play_video(file_path):
    # 創建 VLC 播放器實例
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(file_path)
    player.set_media(media)
    player.play()
    
    while player.get_state() != vlc.State.Ended and not stop_playback:
        time.sleep(1)
    
    if stop_playback:
        player.stop()

file_path = './mp3/rick_roll.mp3'


try:
    # 創建並啟動播放線程
    play_thread = threading.Thread(target=play_video, args=(file_path,))
    play_thread.start()

    # 主迴圈，模擬其他工作
    for i in range(10):
        print(f"Running loop iteration {i+1}")
        time.sleep(1)

except KeyboardInterrupt:
    stop_playback = True
    play_thread.join()

print("Playback stopped.")