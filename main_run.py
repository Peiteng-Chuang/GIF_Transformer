import GTA
import time
import os
import sys
import vlc
import threading
import time

# 設置 VLC 的安裝路徑，這裡應該是包含所有 VLC DLL 文件的目錄
vlc_path='C:/Program Files/VideoLAN/VLC'
file_path = './mp3/rick_roll.mp3'

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

if __name__=="__main__":
    g=GTA.GTA()
    g.clear_save_path()         #removing old stuff in file
    g.save_frames()             #saving new stuff in file
    for i in range(3,1,-1):
        g.clear_screen()
        print(f"即將開始撥放影片...{i}\n請確保有足夠空間顯示動畫")
        time.sleep(1)
    try:
        # 創建並啟動播放線程
        play_thread = threading.Thread(target=play_video, args=(file_path,))
        play_thread.start()

        # 主迴圈，模擬其他工作
        g.dancing()

    except KeyboardInterrupt:
        stop_playback = True
        play_thread.join()
    print("Playback stopped.")

