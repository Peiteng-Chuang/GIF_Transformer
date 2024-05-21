import GTA
import time

if __name__=="__main__":
    g=GTA.GTA()
    g.clear_save_path()         #removing old stuff in file
    g.save_frames()             #saving new stuff in file
    for i in range(5,1,-1):
        g.clear_screen()
        print(f"即將開始撥放影片...{i}\n請確保有足夠空間顯示動畫")
        time.sleep(1)
    g.dancing()
